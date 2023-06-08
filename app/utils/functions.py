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

    credentials = service_account.Credentials.from_service_account_file('utils/token_gcp.json', )    
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
        height= 450
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df_filtered = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df  

    return df_filtered

# def read_sheets_data():
#     # Configura as credenciais
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

#     # Autenticação de usuário
#     client = gspread.authorize(credentials)

#     # Abre a planilha
#     planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

#     # Seleciona a aba desejada
#     aba = planilha.sheet1

#     # Obtém todos os valores da tabela
#     dados = aba.get_all_values()

#     # Transforma os dados em um dataframe
#     df = pd.DataFrame(dados[1:], columns=dados[0])

#     return df

# def insert_new_Data_in_sheets(df):
#     current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Defina o escopo da API e as credenciais do serviço
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

#     # Autorize e abra a planilha
#     client = gspread.authorize(credentials)

#     # Abre a planilha
#     planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

#     # Seleciona a aba desejada
#     aba = planilha.sheet1

#     # Dados para adicionar
#     novos_dados = [
#         [current_datetime,df['Respostas'][0], df['Respostas'][1], df['Respostas'][2],df['Respostas'][3],df['Respostas'][4], df['Respostas'][5],
#          df['Respostas'][6], df['Respostas'][7], df['Respostas'][8], df['Respostas'][9], df['Respostas'][10], df['Respostas'][11],
#          df['Respostas'][12]
#          ]

#     ]

#     # Encontre a próxima linha vazia
#     proxima_linha = len(aba.get_all_values()) + 1
#     #append
#     aba.update(f'A{proxima_linha}', novos_dados)

# def insert_only_proposal_data_in_sheets(df_filtered,df_form):
#     # Defina o escopo da API e as credenciais do serviço
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

#     # Autorize e abra a planilha
#     client = gspread.authorize(credentials)

#     # Abre a planilha
#     planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

#     # Seleciona a aba desejada
#     aba = planilha.sheet1

#     # Obtém todos os valores da tabela
#     dados = aba.get_all_values()

#     # Transforma os dados em um dataframe
#     df_all = pd.DataFrame(dados[1:], columns=dados[0])

#     #filter aggrid
#     df_loc = df_all.loc[df_all['Descreva o problema ou desafio:'].values == df_filtered['Descreva o problema ou desafio:'].values]

#     linha = df_loc.index[0] + 2

#     # Obtenha os dados existentes da linha
#     dados_existentes = aba.row_values(linha)

#     # Novos dados a serem adicionados
#     novos_dados = [df_form['Respostas'][0], df_form['Respostas'][1], df_form['Respostas'][2],df_form['Respostas'][3],
#                    df_form['Respostas'][4], df_form['Respostas'][5], df_form['Respostas'][6],df_form['Respostas'][7],
#                    df_form['Respostas'][8], df_form['Respostas'][9], df_form['Respostas'][10],df_form['Respostas'][11],
#                    df_form['Respostas'][12],df_form['Respostas'][13]
#                    ]

#     # Combine os dados existentes e os novos dados
#     dados_combinados = dados_existentes + novos_dados

#     # Atualize a linha com os dados combinados
#     aba.update(f'A{linha}', [dados_combinados])



