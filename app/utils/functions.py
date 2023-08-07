import streamlit as st
import json

import pandas as pd
from datetime import datetime


from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode,ColumnsAutoSizeMode
#import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas_gbq

def querybq(table):
    """run big query scripts and bring data

    Returns:
        data from big query 
    """

    json_file = {
  "json_secret_past"
    }
    json.dump(json_file, open("json_file.json", 'w'))
    credentials = service_account.Credentials.from_service_account_file( 'json_file.json', )    

    #credentials = service_account.Credentials.from_service_account_file('token_gcp.json', )    
    pandas_gbq.context.credentials = credentials

    if table == 'historical_data':
        sql = """ SELECT  *   FROM `teste-315517.teste.raw_from_linkedin`  """
        project_id = 'teste-315517'
        df = pd.read_gbq(sql, project_id=project_id, dialect='standard')

        return df

def build_aggrid_table(df):
    """Aggrid table is a dinamic table function that improve usability of users.
    This function make simple your implementation

    Args:
        df (dataframe): dataframe to transformed in dinamic table

    Returns:
        printed dinamic table: printed where the function was called
        table filtred if one row was selected: dataframe
    """


    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection(use_checkbox=True) #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        width='100%',
        height= 450,
        filters=True
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df_filtered = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df  

    return df_filtered



