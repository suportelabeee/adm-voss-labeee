import streamlit as st
import smtplib
import email.message
from random import randint
import json
import requests
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
from time import sleep
from datetime import datetime
from os import remove

# ---------------VARIÁVEIS---------------

project = "VOSS"

credentials = json.loads(st.secrets['CREDENTIALS'])
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(credentials, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = st.secrets['SHEET_ID']

workbook = client.open_by_key(sheet_id)
worksheet_build = workbook.worksheet('build')

support_mail = "escritorios.qai.bot@gmail.com"

password = st.secrets['PASSWORD']

authorization_list = st.secrets["AUTH_LIST"]

injection = st.secrets['INJECTION']

cep_link = "https://viacep.com.br/ws/{}/json/"

quest_link = 'https://voss-labeee.streamlit.app/'

support_mail = "escritorios.qai.bot@gmail.com"

# ---------------------------------------


def initialize_page():
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        [data-testid="stToolbarActions"] {
            display: none
        }
        }
        [data-testid="stHeader"] {
            display: none;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True,)


def footer():
    st.title('')
    col1, _, col2, col3 = st.columns(4)
    col1.image(r'static/lab_banner.png', width=300)
    col2.markdown(f"[SOBRE NÓS](https://voss-labeee.streamlit.app/SobreNos)")
    col3.markdown(f"[SUPORTE](mailto:{support_mail})")


def register_building(values_list: list):
    worksheet_build.append_row(values_list)


def check_for_injection(items: list):
    for item in items:
        if item in injection:
            return "INJECTION"
    return "OK"


def get_build_info_by_id(id_: int, email: str):
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    sql = f'SELECT * FROM build WHERE "id" = {id_} AND "email" = \'{email}\''
    response = conn.query(sql)
    if response.empty:
        return None, "ERROR"
    return response, "OK"


def verify_build_exists(cep, numero, complemento, ocupacao, ocupacao_desc, aplicada_toda_ocupacao):
    items = [cep, numero, complemento, ocupacao, ocupacao_desc, aplicada_toda_ocupacao]
    if check_for_injection(items) == "INJECTION":
        return False
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    sql = f'SELECT * FROM build WHERE "cep" = {cep} AND "numero" = \'{numero}\' AND "complemento" = \'{complemento}\' AND "ocupacao" = \'{ocupacao}\' AND "ocupacao-desc" = \'{ocupacao_desc}\' AND "aplicada-toda-ocupacao" = \'{aplicada_toda_ocupacao}\''
    response = conn.query(sql)
    if response.empty:
        return "OK"
    return False

def generate_build_code():
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    sql = f'SELECT MAX(id) AS id FROM build'
    response = conn.query(sql)
    code = int(response["id"].tolist()[0]) + 1
    return code

def mail_auth_code(mail_person:str):
    auth_code = authorization_list[randint(0, len(authorization_list)-1)]
    corpo_email = f"""
    <p>Este é o seu código de verificação para se cadastrar como administrador<p>
    <h1><strong>{auth_code}</strong></h1>
    <p>Insira este código na página do ADM e informe os dados necessários para criar o ID do local de trabalho.</p>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CÓDIGO DE VERIFICAÇÃO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return auth_code


def mail_auth_code_searchpage(mail_person:str):
    auth_code = authorization_list[randint(0, len(authorization_list)-1)]
    corpo_email = f"""
    <p>Este é o seu código de verificação para buscar seu local de trabalho<p>
    <h1><strong>{auth_code}</strong></h1>
    <p>Caso você não tenha solicitado este código, basta ignorar este email.</p>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CÓDIGO DE VERIFICAÇÃO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return auth_code


def confirmation_email(mail_person:str, id_: str, data: str):
    corpo_email = f"""
    <h2>Seu local de trabalho foi cadastrado com sucesso.</h2>
    <p>Este é o ID do seu local de trabalho:</p>
    <br>
    <h1><strong>{id_}</strong></h1>
    <br>
    <p><strong>Informe o ID do local de trabalho para todos os participantes da pesquisa. Este código será necessário para acessar o questionário.</strong></p>
    <p>O ID do local de trabalho é único e refere-se aos seguintes dados informados:</p>
    <li style="color: #b7b7b7;">{'</li><li style="color: #b7b7b7;">'.join(data)}</li>
    <p>Você pode usar este ID sempre que desejar avaliar o mesmo local de trabalho.</p>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CONFIRMAÇÃO DE CADASTRO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


def mailto(participants: list, id_: str):
    corpo_email = f"""
    <h1>Você foi convidado a avaliar o seu local de trabalho.</h1>
    <p><a href={quest_link}>Clique aqui para acessar o questionário</a> e informe o ID do seu local de trabalho:</p>
    <h2><strong>{id_}</strong></h2>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""    
    participants = participants.split(",")
    for participant in participants:
        msg = email.message.Message()
        msg['Subject'] = f'CONVITE - {project}, LabEEE'
        msg['From'] = 'escritorios.qai.bot@gmail.com'
        msg.add_header('Content-Type', 'text/html')
        s = smtplib.SMTP('smtp.gmail.com: 587')
        msg.set_payload(corpo_email)
        s.starttls()
        s.login(msg['From'], password)
        msg['To'] = participant
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


## STREAMLIT_EXTRAS --> switch page button
def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")