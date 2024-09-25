import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state='collapsed', page_title=f"ADM - VOSS", page_icon = '📝')
from utils.config import *

initialize_page()

st.markdown('#')

col1, col2 = st.columns([5,1])
if col2.button(label="Ir para o dashboard", use_container_width=True):
    switch_page("ADM_plotpage")
if col2.button(label="Verificar meu local de trabalho", use_container_width=True):
    switch_page("ADM_searchpage")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.title("ADMINISTRADOR")
col1, col2, col3 = st.columns([1.9,1.7,2])
col2.subheader("Para conectar-se ao seu local de trabalho,")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.subheader("preencha os campos abaixo:")
logo, content = st.columns([1,3])
logo.image(r'static/voss-01.png')
with content:
    st.title("")
    st.write("")
    form_email = st.container(border=True)
    form_email.title("")
    col1, col2 = form_email.columns([4,1])
    email = col1.text_input(label="Email").strip()
    col2.subheader('')
    if col2.button(label="Enviar código de verificação", use_container_width=True):
        try:
            st.session_state['auth_code'] = mail_auth_code(email)
            st.session_state['email'] = email
        except:
            st.error('Um erro ocorreu ao tentar enviar o email de verificação. Verifique se o email inserido está correto e tente novamente', icon="⚠️")
    codigo = form_email.text_input(label="Código", max_chars=6)
    with form_email.expander("**Termos e condições**"):
        col1, col2 = st.columns([4,1])
        st.markdown("""**PARA ADMINISTRADORES**

Esta pesquisa tem caráter anônimo, não sendo possível identificar quaisquer informações que façam referência a nenhum indivíduo, empresa e/ou edificação individualmente.

Os dados sensíveis de cadastro são anonimizados antes de serem adicionados à base, armazenada em nuvem privada e não compartilhada.

**PARA OS PARTICIPANTES**
As questões a serem respondidas são de caráter e preferência pessoais. No entanto, é importante destacar que nenhum(a) participante será identificado(a) em nenhum momento.

Além disso, a participação é totalmente voluntária. É possível abandonar a pesquisa a qualquer momento, sem quaisquer prejuízos, mesmo após o consentimento e de já ter iniciado a participação. Nesse caso, as respostas não serão computadas.

Não haverá qualquer tipo de remuneração pela participação nesta pesquisa, assim como não será gerado qualquer tipo de despesa.

**RISCOS**

Os possíveis riscos decorrentes da aplicação da VOSS são mínimos, e estão listados a seguir:
1. cansaço ou aborrecimento ao responder questionário;
2. evocar memórias e mobilizar sentimentos nem sempre agradáveis;
3. quebra de sigilo em relação às informações fornecidas. Caso ocorra, e mesmo que seja uma possibilidade remota, a quebra de sigilo de dados é involuntária e não intencional. Os pesquisadores envolvidos se comprometem a tomar todos os cuidados necessários para que tal possibilidade não ocorra.

**BENEFÍCIOS**

Reforçamos que os benefícios decorrentes da aplicação da VOSS são de cunho educacional e científico, que por sua vez podem trazer benefícios para a sociedade em geral.

Junto às demais contribuições, será fundamental para agregar conhecimento sobre a satisfação dos ocupantes com parâmetros da Qualidade Ambiental Interna em ambientes de escritório, de forma que as informações coletadas permitam compreender melhor a percepção e o comportamento das pessoas nestes ambientes, levantando pontos críticos que possam ser aprimorados e favorecendo o conforto, a saúde e o bem-estar dos ocupantes.

**Ao selecionar “Eu li e estou de acordo”, você consente a participação nesta pesquisa, sob os termos aqui expostos.**
""")
        st.title("")
        cols = st.columns([1,0.5,1])
        agree_termos = cols[1].checkbox(label="**Eu li e estou de acordo**")
        st.title("")
    col1, col2, col3 = form_email.columns(3)
    if col2.button(label="Validar código", use_container_width=True):
        if not st.session_state.get('auth_code'):
            st.error('ERRO: O código de verificação não foi gerado', icon="⚠️")
        elif not agree_termos:
            st.error('Você deve aceitar os termos e condições para prosseguir', icon="⚠️")
        elif st.session_state['auth_code'] == codigo:
            switch_page("ADM_edificio")
        else:
            st.error('ERRO: O código inserido é diferente do código enviado', icon="⚠️")
    
footer()