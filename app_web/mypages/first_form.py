import streamlit as st
import pandas as pd
import requests

from utils import functions

def show_page(params):
    """Returns `True` if the user had the correct password."""
    col1, col2, col3 = st.columns([0.1, 1, 0.1])
    col2.header("Formulário de solicitação de proposta")
    col2.subheader("O formulário pode ser preenchido e enviado separadamente com as respostas de negócio e respostas técnicas")


    # Perguntas e opções de resposta
    questions = [
        "Descreva o problema ou desafio:",
        "Qual o impacto que esse projeto pode gerar? Existem KPIs para mensurar?",
        "A empresa já realiza a atividade hoje? Se sim, como é feito?",
        "O que espera como entregável final?",
        "Já possui banco de dados?",
        "Já possui cloud?",
        "Possui time técnico em dados?",
        "Qual a expectativa/necessidade de tempo de entrega do projeto? Em meses totais:",
        "Pode compartilhar exemplo dos dados?",
        "Há alguma especificidade técnica para o desenvolvimento? Por exemplo, ser desenvolvido local.",
        "Nome da empresa:",
        "Já sabe qual tipo de profissional precisa? DS, DE, BI ou sistemas:",
        "Será necessário conectar fontes de dados a solução?"
    ]
    # Create a form
    # Respostas
    col1, col2, col3 = st.columns([1, 1, 1])
    col2.subheader('Respostas de Negócio')

    col1, col2 = st.columns([1, 1])
    answer_10 = col1.text_area(questions[10])
    answer_0 = col2.text_area(questions[0])

    answer_1 = col1.text_area(questions[1])   
    #answer_3 = col2.text_area(questions[3])
    answer_3 = col2.multiselect('O que espera como entregável final? exemplo: algoritmo de IA em um BI, marque as 2 alternativas', ['BI', 'Sistema personalizado', 'Banco de dados', "Somente automações", "Algoritmo de IA", 'Outros'])
    if 'Outros' in answer_3:
        answer_3_details = st.text_area('Informe mais detalhes de como gostaria do entegável final do projeto:')
    
    answer_2 = col1.selectbox(questions[2], ('','Não', 'Sim'))
    if answer_2 == 'Sim':
        answer_2_details = st.text_area('Informe mais detalhes de como é feita a atividade hoje:')
    
    answer_7 = col2.number_input(questions[7],step=1)

    answer_8 = st.selectbox(questions[8], ('','Não', 'Sim'))
    if answer_8 == 'Sim':
        #st.file_uploader('Faça upload do dado de exemplo',type=['xlsx','csv','pdf'])
        st.write('Envie um email para mardo.carneiro@bix-tech.com anexando os dados de exemplo')

    col1, col2, col3 = st.columns([1, 1, 1])
    col2.subheader('Respostas Técnicas')
    col1, col2 = st.columns([1, 1])
    answer_4 = col1.selectbox(questions[4], ('','Não', 'Sim'))
    if answer_4 == 'Sim':
        answer_4_details = st.text_area('Informe mais detalhes sobre o banco de dados atual:')
    answer_5 = col2.selectbox(questions[5], ('','Não', 'Sim'))
    if answer_5 == 'Sim':
        cloud_providers = st.multiselect('Selecione o provedor de nuvem:', ['Google Cloud', 'Azure', 'AWS', 'Outros'])

    answer_6 = col1.selectbox(questions[6], ('','Não', 'Sim'))
    if answer_6 == 'Sim':
        answer_6_details = st.text_area('Informe mais detalhes sobre a equipe técnica atual:')
    
    answer_9 = col2.selectbox(questions[9], ('','Não', 'Sim'))
    if answer_9 == 'Sim':
        answer_9_details = st.text_area('Informe mais detalhes sobre as especificidades técnicas:')

    answer_11 = col1.selectbox(questions[11], ('','Não', 'Sim'))
    if answer_11 == 'Sim':
        answer_11_details = st.multiselect('Selecione o/os times definidos', ['Data Science', 'Data Engeneering', 'Business Intelligence', 'Software Development'])
    
    answer_12 = col2.selectbox(questions[12], ('','Não', 'Sim'))
    if answer_12 == 'Sim':
        answer_12_details = st.multiselect('Quais serão as fontes de dados', ['Banco de dados estruturado', 'Banco de dados não estruturado', 'API', 'Excel local', "Drive", "Outro"])
        
    
    if st.button('Enviar formulário'):

        # Transforma as respostas em um dataframe
        df = pd.DataFrame({
            "Perguntas": questions,
            "Respostas": [answer_10,answer_0, answer_1, answer_2 + ' ' + answer_2_details if answer_2 == 'Sim' else answer_2,
                        answer_3 + ' ' + ', '.join(answer_3_details) if answer_3 == 'Sim' else answer_3,
                         answer_4 + ' ' + answer_4_details if answer_4 == 'Sim' else answer_4,
                        answer_5 + ' ' + ', '.join(cloud_providers) if answer_5 == 'Sim' else answer_5,
                        answer_6 + ' ' + answer_6_details if answer_6 == 'Sim' else answer_6,
                        answer_7, answer_8, answer_9 + ' ' + answer_9_details if answer_9 == 'Sim' else answer_9,
                        answer_11 + ' ' + ', '.join(answer_11_details) if answer_11 == 'Sim' else answer_11,
                        answer_12 + ' ' + ', '.join(answer_12_details) if answer_12 == 'Sim' else answer_12
                        ]
        })

        st.header("Respostas do Formulário")
        st.dataframe(df)
        functions.insert_new_Data_in_sheets(df)



