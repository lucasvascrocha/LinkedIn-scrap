import streamlit as st

def show_page(params):

    col1, col2,col3 = st.columns([1, 1, 1])


    col2.image("images/contato.png")

    col2.write('Telefone: (48) 99659 5490')
    col2.write('Email: contato@bixtecnologia.com.br')
    col2.write('Site: https://bixtecnologia.com.br/')
    