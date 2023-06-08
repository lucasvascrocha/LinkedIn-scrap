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
  "type": "service_account",
    "project_id": "teste-315517",
    "private_key_id": "5bbff34ee810ff839e02e3c3a3c8d49c79fee96a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCnTrVXSqljn/bb\ngyYYWukix8QOQ0SWYWx3X10C+UcwVWs2X/8VRro+HkPKK8R7AJxd2UHqef+4exzj\npWtqhBkrsQ7ewkLZBlmZdPho313qZPT7oVZejwy7WhGstObY8ofZzPwAQsi/rSfa\n9H3w1HCeBfvN1/ZY6nL1vdupfFSMdQcmnZC4t+rkty0Cpuddx25Sz5fWQfrGRKJp\n/yw9XlQBmH5w1wLO7vB0aQISdsfG0Zbp7hXyFB8aKT9r1bXGVVDsTh948cF2XceX\njfcVv1hC2zjgbRlPNsNzCQWcU0PQbn3jYj8ibEZCMag0265GZA5yvs7O3x1U0Sb2\nPZo0MkeBAgMBAAECggEAM3NW/QMu2D5HMfZA7th2PYXlWuWA4CYRrxwahGGYbNq3\n377huO9JMvUnr7KJ97GWZJ39UVg3NcpWdgNW5yi8fN00T3i6CfeT8kcwZT/bp8to\nM0HIR8gCCFOIf+4Z17mt4WLSVFo1Vgyv5vutBzStdUstxn2Ven6O39eFB7f+YDrV\nqD3MfP1Bx0d6xHEO19KEm46KHCwgzQy0nrYD1R+b+EA/0BLhwOm66jGQlVIl/CAH\nX0JIoJblUCAaZW9H/pZVZ1Bg6y5FE0ibzp7WFETSi+0Vg4jEQFb5XLUinkHqOlqx\nOIcLbBWKF55MDlQAx78b5dVI7JBR31xVi6Jc9TjTaQKBgQDTmy6BtT23C47EiyPJ\nJDdDI95HmfPX7dmjs6bBt55WfwoY5Uu9jWJ/zBvLku1PS1dLdXELVNDFkOR7l/Af\n4zw8zZPSQHJ5ETdrFoJjVTlgv1LEjM39/A9bp6FBst8GvR9Nm/Q2A5pIikIfnUK0\n+jPVTXVYwYktdvAC0SFz0AyadwKBgQDKaFt2bMGhQhZe0G4EH5UkecT2KwB2aS2s\nSE+YCFxqpiUevSzlOuYyKeIfn3yF8XScTQOvp8/c1qhk8r3pPZWPaXhf0oJG+meW\nAQY7vLoClKKGwysp8ZXklb61KOHNMOtNzw97K/ewX3J/T8dSn2Oe7dbttWuz95yJ\nr8stvQOzxwKBgQDSiz0i4eqeDmnnNWpN4DL8Itwv8galeotqTn5FkSWCerTZQIyz\n9dFjxvqA+5gTpasd8aSg2atAaIJuVycdE0QEW6gRMv6zZ2X0r1jc7RdCJBt+ZXsw\nk3PUhl30uL0gP1y+I8ZBWCRSuP5B5n9RAwI/4eo4fZi4G/eDVgIq8X8Y0QKBgQCP\niR/LRGavv5jzleVewTLXkg7N70K9teqwsPrYup0m+Dl8qfTLflA+JJt5h3Ub21Wx\nfZ/ukheC6Sqzo7xvSb/k2ouFkFfYk7yfkIxmEnjqWZND8+WJMgv09QgvmhU+mMFV\nBVBaLZzRk24zwFR+UA+qZcmz+qKtFhwJPAPepJqagwKBgEzHncDt78n5okj4MK6c\nfgdEkM5AlCMqo0NIWmXoWXLoRVMZvfJjsTjX74UwvVbmEn5rE584lqcDr3IiM6dc\nM2vm8s6WKinulBAAX3+kZhkdS26gXCIhGSaoKauEgy59WBOtwelzJYlc2xrW5tA2\nKpd1CMCW9EQ+jgLTKBKSfKHA\n-----END PRIVATE KEY-----\n",
    "client_email": "teste-315517@appspot.gserviceaccount.com",
    "client_id": "117692008242796046619",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/teste-315517%40appspot.gserviceaccount.com",
    "universe_domain": "googleapis.com"
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



