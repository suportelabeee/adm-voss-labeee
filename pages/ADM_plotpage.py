import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state='collapsed', page_title=f"ADM - VOSS", page_icon = '📝')
from utils.config import *

initialize_page()

st.title("Dashboards")
st.header("Ainda em desenvolvimento...")
st.title("")

st.title("")
st.title("")
col1, col2, col3 = st.columns(3)
if col2.button(label='Voltar à página inicial', use_container_width=True):
    switch_page('ADM_firstpage')

footer()