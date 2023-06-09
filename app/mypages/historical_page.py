import streamlit as st
from utils import functions
import re

def show_page(params):
    """Returns `True` if the user had the correct password."""

    table = 'historical_data'
    df_cleaned = load_and_preprocess_data(table)
    df_cleaned = df_cleaned.sort_values('now_datetime',ascending=False)
    df_cleaned = df_cleaned.rename({'now_datetime': 'date'},axis=1)

    avoid_lag = True

    if avoid_lag:

        col1, col2, col3 = st.columns([1,1,1])   
        col2.subheader('Show all historical collected data')   
        with st.expander("Instructions to use"):
            st.write('You can apply multiple filters using the Filters tab. E.g., select the description column and type "GCP" hit enter, then type "VERTEX" hit enter, and so on.')
            st.write("You can see the complete description and link by clicking the vacancy's checkbox.")
            st.write('You can filter by date.')

        df_filtered = functions.build_aggrid_table(df_cleaned)

    if len(df_filtered)>0:
        col1, col2, col3 = st.columns([0.1,1,0.1])   
        col2.write(df_filtered['link'].values[0])
        col2.write(df_filtered['description'].values[0])

        st.dataframe(df_filtered.iloc[:, 1:],use_container_width=True)
    else:
        st.write('Select one job row to see full details.')


def load_and_preprocess_data(table):
    df = functions.querybq(table)
    df_cleaned = clean_column_strings(df)


    return df_cleaned

def word_split(text):
    """Split some words that are imprecisaly toguether after scrap

    Args:
        text (string): string to process

    Returns:
        string: string processed
    """
    # replaces each uppercase letter with a space followed by the same lower case letter

    #text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    valor_limpo = re.sub('<[^<]+?>', '', text)

    #return text.strip()
    return valor_limpo.strip()

def clean_column_strings(df):
    """Clean each column of a dirty dataframe

    Args:
        df (dataframe): dataframe to be clean

    Returns:
        dataframe: cleaned dataframe
    """
    
    #df['location'] = df['location'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    #df['company_name'] = df['company_name'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    #df['experience_required'] = df['experience_required'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    #df['contract_type'] = df['contract_type'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    #df['function_name'] = df['function_name'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    #df['company_sector'] = df['company_sector'].apply(lambda x: x.replace("\n", "").strip() if type(x) == str else x)
    clean = re.compile('<.*?>')
    df['description'] = df['description'].apply(lambda x: re.sub(clean, '', x).replace('\n','').strip())
    df['description'] = df['description'].apply(lambda x: word_split(x))
    
    return df