import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from utils.estado import (
    fazer_logout,
    inicializar_estado,
    recarregar_salas,
    usuario_logado,
)
from utils.componentes import injetar_css
from views.login_view import pagina_login
import main


st.set_page_config(
    page_title="Reserva de Salas",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

injetar_css()
inicializar_estado()
recarregar_salas()

usuario = usuario_logado()

if usuario is None:
    pagina_login()
    st.stop()


with st.sidebar:
    st.markdown("Reserva de Salas")
    st.divider()

    st.markdown(f"### {usuario['nome']}")
    st.caption(f"Conta de {usuario['tipo']}")

    st.divider()
    st.markdown("### Menu")

    pagina = st.radio(
        "Navegação",
        main.menu_para(usuario["tipo"]),
        label_visibility="collapsed",
    )

    st.divider()

    if st.button("Sair"):
        fazer_logout()
        st.rerun()


main.render_pagina(pagina, usuario)