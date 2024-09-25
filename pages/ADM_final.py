import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state='collapsed', page_title=f"ADM - VOSS", page_icon = '📝')
from utils.config import *

initialize_page()

col1, col2, col3 = st.columns([1,1.5,1])
if col1.button('Voltar ao início'):
    switch_page("ADM_firstpage")

st.title("")

st.subheader('Este é o ID do seu local de trabalho:')
st.title(st.session_state.get("build_id"))
st.markdown("O ID do local de trabalho é único. Você pode utilizá-lo sempre que desejar avaliar o mesmo local de trabalho.")
st.title("")
data_review_c = st.container(border=True)
try:
    if_date = st.session_state.get('check_answers')[-1]
    if_date = datetime.strptime(if_date, '%Y-%m-%d %H:%M:%S.%f')
    if_date = if_date.strftime('%d/%m/%Y %H:%M')
    if_date = f', registrados em {if_date}'
except:
    if_date = ''
data_review_c.markdown(f"Este ID refere-se aos seguintes dados informados{if_date}:")
col11, col21 = data_review_c.columns(2)
st.session_state['check_answers'][0] = int(st.session_state['check_answers'][0])
parte1, parte2 = st.session_state.get('check_answers')[:7], st.session_state.get('check_answers')[7:]
col11.markdown(f"- CEP: {parte1[0]}\n- Endereço: {parte1[1]}\n- Número: {parte1[2]}\n- Complemento: {parte1[3]}\n- Bairro: {parte1[4]}\n- Cidade: {parte1[5]}\n- Estado: {parte1[6]}")
desc_trecho_pavimento = f"- Pavimento(s): {parte2[2]}\n" if parte2[1] != 'Trecho de um pavimento' else ''
col21.markdown(f"- Local de trabalho: {parte2[0]}\n- Ocupação: {parte2[1]}\n{desc_trecho_pavimento}- Aplicação em todo o trecho: {parte2[3]}\n- Trecho: {parte2[4]}")
st.title("")
st.subheader("Informe o ID do local de trabalho para todos os participantes da pesquisa.")
st.markdown("Este código será necessário para acessar o questionário.")
st.title("")
participants = st.text_input(label="Insira a lista de emails no campo abaixo para convidar os participantes da pesquisa automaticamente:", placeholder='Escreva os emails separados por vírgula')
_, col = st.columns([3,1])
if col.button(label='Enviar emails', use_container_width=True):
    try:
        with st.spinner("Enviando emails..."):
            mailto(participants=participants, id_=st.session_state.get("build_id"))
        st.success("Emails enviados com sucesso!", icon="✅")
    except Exception as e:
        st.error('Houve um problema ao enviar os emails', icon="⚠️")

st.title("")

st.markdown("Se preferir, copie a mensagem abaixo no seu email:")
st.code(body=f"""Você foi convidado a avaliar o seu local de trabalho.
Acesse o questionário através do link {quest_link} e informe o ID do seu local de trabalho:
{st.session_state.get('build_id')}""", line_numbers=True)

footer()