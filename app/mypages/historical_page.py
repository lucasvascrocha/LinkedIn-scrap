import streamlit as st
from utils import functions

def show_page(params):
    """Returns `True` if the user had the correct password."""

    col1, col2, col3 = st.columns([1,1,1])   
    col2.subheader('Show all historical collected data')

    table = 'historical_data'
    df = functions.querybq(table)
    st.write(df.info())
    st.dataframe(df)
