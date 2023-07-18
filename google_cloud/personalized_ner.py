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
    """Get ids for query in bigquery in a all table joined.

    Args:
        input (tuple): JSON with id (unique id from Pipedrive)

    Returns:
        json: JSON with data consulted in bigquery
    """
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    query_result = read_bq_table()

    query_result = spacy_extract(query_result)

    query_result = query_result.drop(['clean_description'], axis=1)

    query_result = query_result.rename(columns={'description': 'description_full'})

    save_in_bq(query_result)
    
    #passing the order of the columns to preserve sort columns
    #df_transposed = query_result.T.reset_index().reset_index()

    #result = df_transposed.to_json(orient="records")
    #output = json.loads(result)

    #return jsonify(output)
    return 'finish'


def save_in_bq(df_to_save_in_cloud):
    google_credentials = service_account.Credentials.from_service_account_file(
    'credentials.json')
    project_id = 'teste-315517'
    bq_client = bigquery.Client(credentials= google_credentials,project=project_id)

    #save data in BigQuery table
    table_id = 'teste-315517.teste.ner_from_linkedin'

    #transform everything in string for avoid problemns in bigquery writing
    df = df_to_save_in_cloud.astype(str)

    job = bigquery_client.load_table_from_dataframe(
    df, table_id)


def spacy_extract(query_result):

    # # Verificar se o modelo 'en_core_web_lg' está instalado

    # Caso não esteja instalado, fazer o download e instalação
    subprocess.run(['python3', '-m', 'spacy', 'download', 'en_core_web_lg'])

    #command = f'python -m spacy download en_core_web_lg'
    #output = subprocess.check_output(command, shell=True)
    #command = ["pip3", "install", "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz"]
    #subprocess.run(command, check=True)
    print('run subprocess')
    import en_core_web_lg
    nlp = en_core_web_lg.load()
    #nlp = spacy.load('en_core_web_sm')
    print('loaded mdoel')

    #NER model personalized
    #nlp = spacy.load("en_core_web_sm")
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