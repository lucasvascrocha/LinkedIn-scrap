import functions_framework
from flask import jsonify
import json
import requests
from google.cloud import bigquery
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

#spacy
import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.tokens import Doc

#nltk
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords','wordnet'])

import subprocess
import jsonlines


@functions_framework.http
def ner_personalized(request):
    """
    Endpoint function for Named Entity Recognition (NER) with personalized patterns.

    This function is an HTTP endpoint designed for Named Entity Recognition (NER) using
    personalized patterns. It takes an HTTP request as input, processes the data, and 
    performs NER using the 'spacy_extract' function. The results are saved to a BigQuery 
    table using the 'save_in_bq' function.

    Parameters:
        request (flask.Request): An HTTP request object containing data to be processed.

    Returns:
        str: A string indicating the completion of the NER process ('finish').

    Requirements:
        - The function requires the 'flask', 'google-cloud-bigquery', 'pandas', and 'spacy' 
          libraries to be installed.
        - The 'read_bq_table', 'spacy_extract', and 'save_in_bq' functions must be defined 
          and accessible.

    Note:
        - The function uses the 'flask' library for HTTP request handling.
        - The 'spacy_extract' function is used for NER with personalized patterns.
        - The 'read_bq_table' function is used to fetch data from a specified BigQuery table.
        - The 'save_in_bq' function is used to save the NER results to a BigQuery table.
        - The 'query_result' DataFrame is obtained from the 'read_bq_table' function, 
          processed using 'spacy_extract', and then modified (dropping 'clean_description' 
          column and renaming 'description' to 'description_full') before being saved to 
          BigQuery.
    """

    
    request_json = request.get_json(silent=True)
    request_args = request.args

    query_result = read_bq_table()

    query_result = spacy_extract(query_result)

    query_result = query_result.drop(['clean_description'], axis=1)

    query_result = query_result.rename(columns={'description': 'description_full'})

    save_in_bq(query_result)
    
    return 'finish'

def save_in_bq(df_to_save_in_cloud):
    """
    Saves a DataFrame to a BigQuery table in the 'teste-315517' project.

    This function takes a DataFrame 'df_to_save_in_cloud' and saves it to a specified
    BigQuery table named 'ner_from_linkedin' in the 'teste-315517' project.

    Parameters:
        df_to_save_in_cloud (pandas.DataFrame): The DataFrame to be saved to BigQuery.

    Requirements:
        - The function requires the 'google-cloud-bigquery' library to be installed.
        - A 'credentials.json' file with valid Google Cloud service account credentials 
          must be present in the same directory as this script.
        - The 'df_to_save_in_cloud' DataFrame should be properly formatted and have 
          data that can be written to BigQuery.

    Note:
        - The function uses the 'google-cloud-bigquery' library and the 'pandas' library.
        - The 'project_id' is set to 'teste-315517', which needs to be changed to the 
          correct project ID.
        - The 'table_id' is set to 'teste-315517.teste.ner_from_linkedin', which needs 
          to be updated with the desired BigQuery dataset and table name.
        - The function converts all data in the 'df_to_save_in_cloud' DataFrame to 
          strings before saving to avoid writing problems in BigQuery.
    """
    google_credentials = service_account.Credentials.from_service_account_file(
    'credentials.json')
    project_id = 'teste-315517'
    bq_client = bigquery.Client(credentials= google_credentials,project=project_id)

    #save data in BigQuery table
    table_id = 'teste-315517.teste.ner_from_linkedin'

    #transform everything in string for avoid problemns in bigquery writing
    df = df_to_save_in_cloud.astype(str)

    job = bq_client.load_table_from_dataframe(
    df, table_id)


def spacy_extract(query_result):
    """
    Extracts entities from text data using spaCy's NER (Named Entity Recognition) model.

    This function processes the 'clean_description' column from the input DataFrame 
    'query_result', which contains text data. It uses spaCy's 'en_core_web_lg' language 
    model, which should be downloaded and installed if not available.

    The function performs the following steps:
    1. Loads the 'en_core_web_lg' model from spaCy.
    2. Adds a personalized NER model from a JSONL file for additional entity recognition.
    3. Cleans the text data in the 'clean_description' column.
    4. Extracts entities (skills, contracts, educations, constraints) from the cleaned text.
    5. Extracts years of experience from the text using a regular expression pattern.
    6. Formats the extracted entities and returns the resulting DataFrame.

    Parameters:
        query_result (pandas.DataFrame): A DataFrame containing the 'clean_description' 
                                         column with text data to be processed.

    Returns:
        pandas.DataFrame: A DataFrame with the extracted entities, including separate 
                          columns for skills, contracts, educations, and constraints, 
                          along with a 'yrs_experience' column for years of experience.

    Requirements:
        - The function requires the 'spacy' library and the 'en_core_web_lg' model to be 
          installed. If not available, the function will attempt to download and install 
          the 'en_core_web_lg' model.
        - The function depends on the 'clean_description' column in the input DataFrame 
          'query_result' to be present and properly cleaned.

    Note:
        - The 'en_core_web_lg' model is used for NER and language processing.
        - The 'personalized_ner.jsonl' file is expected to contain patterns for additional
          entity recognition using spaCy's 'entity_ruler'.
        - The function may extract entities such as skills, contracts, educations, and 
          constraints from the text data.
        - The function utilizes a regular expression pattern to extract years of experience
          from the text, assuming it is in the format of numbers followed by 'years', 'year',
          'yrs', or 'yr'.
        - The resulting DataFrame will have cleaned text data in the 'clean_description' 
          column and formatted entities in separate columns.
    """

    # download model
    subprocess.run(['python3', '-m', 'spacy', 'download', 'en_core_web_lg'])
    print('run subprocess')
    import en_core_web_lg
    nlp = en_core_web_lg.load()
    print('loaded mdoel')

    #NER model personalized
    skill_pattern_path = "personalized_ner.jsonl"
    #Entity Ruler
    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(skill_pattern_path)

    #clean data
    df_cleaned = clean_description_column(query_result)
    clean = clean_data(df_cleaned)
    data = df_cleaned.copy()

    data['clean_description'] = clean
    data["clean_description"] = data["clean_description"].str.lower()
    #results receive all the entities extracted
    result = data["clean_description"].apply(lambda text: get_all_entities(text,nlp))

    # Access the extracted entities from the result
    all_skills = result.apply(lambda x: x[0])
    all_contracts = result.apply(lambda x: x[1])
    all_educations = result.apply(lambda x: x[2])
    all_constraints = result.apply(lambda x: x[3])

    # add skills extracted in a datafrme
    data["skills"] = all_skills
    data["contract"] = all_contracts
    data["education"] = all_educations
    data["constraints"] = all_constraints

    # Define regular expression pattern to match the number of years
    pattern = r'(\d+)\+?\s*(years|year|yrs|yr)'
    matches = data['clean_description'].apply(lambda x: re.findall(pattern, x, re.IGNORECASE))

    data['yrs_experience'] = matches.apply(lambda x: max([int(match[0]) for match in x]) if x else None).fillna(0)

    data["skills"] = data["skills"].apply(lambda x: ', '.join(x).strip('[]'))
    data["contract"] = data["contract"].apply(lambda x: ', '.join(x).strip('[]'))
    data["education"] = data["education"].apply(lambda x: ', '.join(x).strip('[]'))
    data["constraints"] = data["constraints"].apply(lambda x: ', '.join(x).strip('[]'))

    return data

def read_bq_table():
    """
    Reads data from a BigQuery table using the Google Cloud SDK.

    This function reads data from a specified BigQuery table named 'raw_from_linkedin'
    in the 'teste-315517' project. It retrieves data for the current date, specifically
    the columns 'now_datetime', 'link', and 'description'.

    Returns:
        pandas.DataFrame: A DataFrame containing the query result with columns 
                          'now_datetime', 'link', and 'description'.

    Requirements:
        - The function requires the 'google-cloud-bigquery' library to be installed.
        - A 'credentials.json' file with valid Google Cloud service account credentials 
          must be present in the same directory as this script.

    Note:
        - The function uses the 'google-cloud-bigquery' library and the 'pandas' library.
        - The 'project_id' is set to 'teste-315517', which needs to be changed to the 
          correct project ID.
        - The table name 'raw_from_linkedin' should exist in the specified BigQuery 
          project and dataset.
        - The function executes a SQL query to fetch data for the current date.
        - The 'now_datetime' column is expected to contain timestamps.
    """
    #Google credentials
    google_credentials = service_account.Credentials.from_service_account_file(
        'credentials.json')
    project_id = 'teste-315517'
    bq_client = bigquery.Client(credentials= google_credentials,project=project_id)

    query = f"""
        SELECT 
        now_datetime,
        link,
        description
        FROM `teste-315517.teste.raw_from_linkedin`
        WHERE DATE(now_datetime) = CURRENT_DATE()
            """
    
    #bq_client = bigquery.Client(credentials)
    default_job_config = bigquery.job.QueryJobConfig(
                    use_legacy_sql=False,
                    use_query_cache=True
            )
    query_job = bq_client.query(query, default_job_config)

    query_result = query_job.result().to_dataframe()

    return query_result


def clean_description_column(df):
    """Clean each column of a dirty dataframe

    Args:
        df (dataframe): dataframe to be clean

    Returns:
        dataframe: cleaned dataframe
    """

    clean = re.compile('<.*?>')
    df['description'] = df['description'].apply(lambda x: re.sub(clean, '', x).replace('\n','').strip())
    df['description'] = df['description'].apply(lambda x: word_split(x))
    
    return df

def word_split(text):
    """Split some words that are imprecisaly toguether after scrap

    Args:
        text (string): string to process

    Returns:
        string: string processed
    """
    # replaces each uppercase letter with a space followed by the same lower case letter
    #text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub('<[^<]+?>', '', text)

    return text.strip()

def clean_data(data):
    """
    Cleans the reviews in the given data by performing the following steps:
    1. Removes special characters, URLs, mentions, and RT tags from each review.
    2. Converts the text to lowercase.
    3. Splits the text into individual words.
    4. Lemmatizes the words using WordNetLemmatizer.
    5. Removes stopwords from the text.
    6. Joins the words back into a cleaned review.
    7. Returns a list of cleaned reviews.

    Args:
        data (pandas.DataFrame): The input data containing a "description" column.

    Returns:
        list: A list of cleaned reviews.
    """
    clean = []
    for i in range(data.shape[0]):
        review = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"', " ", data["description"].iloc[i])
        review = review.lower()
        review = review.split()
        lm = WordNetLemmatizer()
        review = [lm.lemmatize(word) for word in review if not word in set(stopwords.words("english"))]
        review = " ".join(review)
        clean.append(review)

    return clean

def get_all_entities(text,nlp):
    """Extracts all entities  from the given text.

    Args:
        text (str): The text from which entities need to be extracted.

    Returns:
        list: A list of entities extracted from the text with the specified label.
    """
    doc = nlp(text)

    skill = []
    contract = []
    education = []
    constraints = []

    for ent in doc.ents:
        if ent.label_ == "SKILL":
            skill.append(ent.text)
        if ent.label_ == "CONTRACT":
            contract.append(ent.text)
        if ent.label_ == "EDUCATION":
            education.append(ent.text)
        if ent.label_ == "CONSTRAINTS":
            constraints.append(ent.text)

    return skill, contract, education, constraints