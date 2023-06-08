import streamlit as st

import pandas as pd
from datetime import datetime


from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection( use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        width='100%',
        height= 400
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df_filtered = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df  

    return df_filtered

def read_sheets_data():
    # Configura as credenciais
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

    # Autenticação de usuário
    client = gspread.authorize(credentials)

    # Abre a planilha
    planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

    # Seleciona a aba desejada
    aba = planilha.sheet1

    # Obtém todos os valores da tabela
    dados = aba.get_all_values()

    # Transforma os dados em um dataframe
    df = pd.DataFrame(dados[1:], columns=dados[0])

    return df

def insert_new_Data_in_sheets(df):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Defina o escopo da API e as credenciais do serviço
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

    # Autorize e abra a planilha
    client = gspread.authorize(credentials)

    # Abre a planilha
    planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

    # Seleciona a aba desejada
    aba = planilha.sheet1

    # Dados para adicionar
    novos_dados = [
        [current_datetime,df['Respostas'][0], df['Respostas'][1], df['Respostas'][2],df['Respostas'][3],df['Respostas'][4], df['Respostas'][5],
         df['Respostas'][6], df['Respostas'][7], df['Respostas'][8], df['Respostas'][9], df['Respostas'][10], df['Respostas'][11],
         df['Respostas'][12]
         ]

    ]

    # Encontre a próxima linha vazia
    proxima_linha = len(aba.get_all_values()) + 1
    #append
    aba.update(f'A{proxima_linha}', novos_dados)

def insert_only_proposal_data_in_sheets(df_filtered,df_form):
    # Defina o escopo da API e as credenciais do serviço
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('utils/token_gcp.json', scope)

    # Autorize e abra a planilha
    client = gspread.authorize(credentials)

    # Abre a planilha
    planilha = client.open_by_key('1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s')

    # Seleciona a aba desejada
    aba = planilha.sheet1

    # Obtém todos os valores da tabela
    dados = aba.get_all_values()

    # Transforma os dados em um dataframe
    df_all = pd.DataFrame(dados[1:], columns=dados[0])

    #filter aggrid
    df_loc = df_all.loc[df_all['Descreva o problema ou desafio:'].values == df_filtered['Descreva o problema ou desafio:'].values]

    linha = df_loc.index[0] + 2

    # Obtenha os dados existentes da linha
    dados_existentes = aba.row_values(linha)

    # Novos dados a serem adicionados
    novos_dados = [df_form['Respostas'][0], df_form['Respostas'][1], df_form['Respostas'][2],df_form['Respostas'][3],
                   df_form['Respostas'][4], df_form['Respostas'][5], df_form['Respostas'][6],df_form['Respostas'][7],
                   df_form['Respostas'][8], df_form['Respostas'][9], df_form['Respostas'][10],df_form['Respostas'][11],
                   df_form['Respostas'][12],df_form['Respostas'][13]
                   ]

    # Combine os dados existentes e os novos dados
    dados_combinados = dados_existentes + novos_dados

    # Atualize a linha com os dados combinados
    aba.update(f'A{linha}', [dados_combinados])




def build_proposal(df_filtered):
       
    col1, col2, col3 = st.columns([0.1, 1, 0.1])

    col2.subheader("Avalie os projetos similares antes de definir como será desenvolvida a proposta atual")

    # Respostas
    col1, col2 = st.columns([1, 1])
    answer_1 = col1.selectbox('O escopo do desafio é aplicável para BIX?', ('','Não', 'Sim'))
    answer_2 = col2.multiselect('Para qual ou quais times seriam necessários para o desenvolvimento deste desafio?', ['Data Science', 'Data Engeneering', 'Business Intelligence', 'Software Development'])

    answer_3 = col1.selectbox('O escopo do projeto será fechado ou aberto?', ('','Aberto', 'Fechado'))
    answer_4 = col2.multiselect('Como estão os dados a serem consumidos?', ['Estruturados em banco de dados', 'Excel local', 'API', "Software terceiro a ser extraído", "Desestruturados", 'Outros'])

    answer_5 = col1.selectbox('É necessário implementar um pipeline de processamento em tempo real ou em lote?', ('','Em lote', 'Tempo real'))
    answer_6 = col2.multiselect('Como será o entregável final?', ['Power BI', 'Qlik Sense', 'Streamlit', 'Sistema personalizado', 'Banco de dados', 'API', 'Excel'])

    answer_7 = col1.selectbox('Defina o escopo técnico do desafio', ('','Regressão', 'Forecast', 'clusterização', 'Recomendação', 'Otimização', 'Visão computacional', 'NLP', 'RPA', 'Scraping'))
    answer_8 = col2.multiselect('Qual ou quais dessas situações mais se enquadram para este projeto?', ['Receberei os dados prontos em banco de dados', 'Receberei os dados prontos em excel', 'Precisarei extrair dados de APIs', 'Precisarei extrair dados de sistemas que desconheço', 'Precisarei configurar pipeline de ingestão de dados em banco de dados ou algoritmo', 'Precisarei desenvolver local', 'Precisarei desenvolver na cloud', 'Precisarei desenvolver orquestração de fluxos','A solução necessitará de integração com softwares já existentes', 'Há requisitos muito específicos para o desenvolvimento', 'Estamos livres para sugerir e desenvolver da forma que propormos'])


    answer_9 = col1.text_area('Demais desenvolvimentos e customizações necessários')   
    answer_10 = col2.text_area('Descreva um texto descrevendo a solução proposta')   

    answer_11 = col1.text_area('Descreva o objetivo geral do projeto')   
    answer_12 = col2.text_area('Demais observações relevantes e específicas')   

    button1 = st.button(label='Estimar tempo de projeto')

    if st.session_state.get('button') != True:

        st.session_state['button'] = button1

    if st.session_state['button'] == True:
        col1, col2, col3 = st.columns([0.1, 1, 0.1])
        col2.subheader("Sugestão de tempo de projeto com base na formulação da proposta")
        #st.write('Entre 4 a 6 meses')
        estimated_weeks = estimation_time(answer_1,answer_2,answer_3,answer_4,answer_5,answer_6,answer_7,answer_8,answer_9,answer_10,answer_11,answer_12)
        col2.write(f"{estimated_weeks} semanas")
       
        
        col1, col2, col3 = st.columns([0.1, 1, 0.1])
        col2.subheader("Cronograma customizado da proposta em semanas")
    
        col1, col2 = st.columns([1, 1])

        step1 = col1.slider("Setup do projeto", 0, 10, 1)
        step2 = col2.slider("ETL", 0, 10, 4)

        step3 = col1.slider("Análise", 0, 10, 3)
        step4 = col2.slider("Modelagem", 0, 10, 6)

        step5 = col1.slider("Produtização", 0, 10, 6)
        step6 = col2.slider("Extra", 0, 10, 0)


        #somatório das etapas
        total_weeks = step1 + step2 + step3 + step4 + step5
        col1, col2, col3 = st.columns([1, 1, 1])
        st.header('')
        col2.write(f"Total em semanas: {total_weeks}")
        col2.write(f"Total em meses: {total_weeks/4}")

        hour_cost = col1.number_input('Valor Hora',0,500,200)
        total_cost = (hour_cost * 44) * total_weeks 
        col2.write(f"Custo total do projeto: R$ {total_cost}")

        if st.button('Salvar formulário'):
             # Transforma as respostas em um dataframe
            df_form = pd.DataFrame({
                "Respostas": [answer_1,
                            ', '.join(answer_2),
                             answer_3,
                              ', '.join(answer_4) ,
                            answer_5,
                            ', '.join(answer_6) ,
                            answer_7,
                            ', '.join(answer_8) ,
                            answer_9,answer_10,answer_11,answer_12,total_weeks,total_cost
                            ]
            })
            insert_only_proposal_data_in_sheets(df_filtered,df_form)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:

                
                st.subheader("Passos para criação do slide da proposta")
                st.subheader("Passo 1: Contato com outros times")
                st.write("Entre em contato com os demais times caso seja um projeto interchapter")
                
                st.subheader("Passo 2: Slide de proposta")
                st.write("Faça um slide de proposta")
                st.write("[Slide de pitch sem solução](https://docs.google.com/presentation/d/1E7EwR0RvXcZJRoqFsqcYG1R43SKArrGP/edit?usp=sharing&ouid=105497879988811146259&rtpof=true&sd=true)")
                
                st.subheader("2.1: Criação de pasta no Drive")
                st.write("Crie uma pasta com o nome do cliente e projeto no drive comercial")
                st.write("[Drive comercial](https://drive.google.com/drive/folders/1qS6Y62dYmSFSER1KtkeTSWUxsC68t542?usp=sharing)")
                
                st.subheader("2.2: Slide exemplificando a solução")
                st.write("Adicione o slide explicando o desafio e a solução proposta")
                
                st.subheader("2.3: Exemplificar a tela final com output")
                st.write("Utilize ferramentas como Figma para exemplificar a tela final com output")
                
                st.subheader("2.4: Detalhar o fluxograma de negócio")
                st.write("Utilize ferramentas de fluxograma como o Miro para detalhar o fluxograma de negócio [Miro DS](https://miro.com/welcomeonboard/QjB1NUNJVzFjRWNEdUdidHQ5cWh6V2NOTDFlSmp2VWRMT1NqSFEwcU16SHRTT2w0M3ZvVkNVclA4VkpPUW1sdXwzMDc0NDU3MzU3MjAzMTI2ODMwfDI=?share_link_id=982849907780)")
                
                st.subheader("2.5: Detalhar o fluxograma técnico")
                st.write("Utilize ferramentas como o [Diagrams.io](http://diagrams.io) para detalhar o fluxograma técnico")
                
                st.subheader("2.6: Detalhar os entregáveis, prazos e custos")
                st.write("Detalhe claramente os entregáveis, prazos e custos")
                
                st.subheader("Passo 3: Envio da proposta")
                st.write("Enviar a proposta para o time comercial")

                st.subheader("Passo 4: Salvar link do drive do projeto na planilha")
                st.write("Salvar o link do drive do projeto na planilha na linha relacionada ao projeto")
                st.write('[planilha](https://docs.google.com/spreadsheets/d/1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s/edit?usp=sharing)')


def estimation_time(answer_1,answer_2,answer_3,answer_4,answer_5,answer_6,answer_7,answer_8,answer_9,answer_10,answer_11,answer_12):
    # Definindo os pesos para cada resposta
    pesos = {
        'Não': 0,
        'Sim': 1,
        'Data Science': 1,
        'Data Engineering': 1,
        'Business Intelligence': 1,
        'Software Development': 1,
        'Aberto': 0,
        'Fechado': 1,
        'Estruturados em banco de dados': 1,
        'Excel local': 1,
        'API': 1,
        'Software terceiro a ser extraído': 1,
        'Desestruturados': 1,
        'Outros': 1,
        'Em lote': 1,
        'Tempo real': 1,
        'Power BI': 1,
        'Qlik Sense': 1,
        'Streamlit': 1,
        'Sistema personalizado': 1,
        'Banco de dados': 1,
        'API': 1,
        'Excel': 1,
        'Regressão': 1,
        'Forecast': 1,
        'Clusterização': 1,
        'Recomendação': 1,
        'Otimização': 1,
        'Visão computacional': 1,
        'NLP': 1,
        'RPA': 1,
        'Scraping': 1,
        'Receberei os dados prontos em banco de dados': 1,
        'Receberei os dados prontos em excel': 1,
        'Precisarei extrair dados de APIs': 1,
        'Precisarei extrair dados de sistemas que desconheço': 1,
        'Precisarei configurar pipeline de ingestão de dados em banco de dados ou algoritmo': 1,
        'Precisarei desenvolver local': 1,
        'Precisarei desenvolver na cloud': 1,
        'Precisarei desenvolver orquestração de fluxos': 1,
        'A solução necessitará de integração com softwares já existentes': 1,
        'Há requisitos muito específicos para o desenvolvimento': 1,
        'Estamos livres para sugerir e desenvolver da forma que propormos': 1
    }

    # Calcular a soma dos pesos das respostas selecionadas
    soma_pesos = 0
    soma_pesos += pesos.get(answer_1, 0)

    for answer in answer_2:
        soma_pesos += pesos.get(answer, 0)

    soma_pesos += pesos.get(answer_3, 0)

    for answer in answer_4:
        soma_pesos += pesos.get(answer, 0)

    soma_pesos += pesos.get(answer_5, 0)

    for answer in answer_6:
        soma_pesos += pesos.get(answer, 0)

    soma_pesos += pesos.get(answer_7, 0)

    for answer in answer_8:
        soma_pesos += pesos.get(answer, 0)

    # Exibir a somatória dos pesos
    return soma_pesos