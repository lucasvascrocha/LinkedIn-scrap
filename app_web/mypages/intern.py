import streamlit as st

from utils import functions
from utils import login

import pandas as pd

def show_page(params):
    
    #if login.check_password():

    col1, col2, col3 = st.columns([0.1, 1, 0.1])
    col2.subheader('Propostas históricas')

    with col2.expander("Alterar dados cadastrados"):
        st.write('altere diretamente na planilha')
        st.write('https://docs.google.com/spreadsheets/d/1hWwbZQ6IhsHlYO-EMKc7DyZMxVZmQCs92f6nZGd6q-s/edit#gid=0')
        st.write('Mantenha o padrão de formatação dentro de cada coluna, evite deixar linhas duplicadas para cada cliente')
        
    df = functions.read_sheets_data()
    df_filtered = functions.build_aggrid_table(df[::-1])

    if len(df_filtered)>0:
        col1, col2,col3 = st.columns([1, 1,1,])
        col2.subheader('Proposta selecionada')
        col2.write('Dê 2 cliques para extender o conteúdo de uma célula')
        st.dataframe(df_filtered.iloc[:, 1:],use_container_width=True)
        col1, col2,col3 = st.columns([1, 1,1,])
        col2.subheader('Formular proposta')
        functions.build_proposal(df_filtered)

            
    else:
        st.write('Escolha um Lead para formular a proposta ou alterar dados de formulário')

    #else:
    #    st.write('Entre com a senha')

    