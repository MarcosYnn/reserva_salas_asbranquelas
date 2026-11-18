
import streamlit as st

try:
    from importlib import import_module

    load_dotenv = import_module("dotenv").load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.estado import (
    inicializar_estado,
    usuario_logado,
    fazer_logout,
    confirmar_email_via_token,
    redefinir_senha_via_token,
)
from utils.componentes import injetar_css
from views.login_view import pagina_login


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Reserva de Salas",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

injetar_css()
inicializar_estado()


# ==========================================
# LINKS RECEBIDOS POR E-MAIL
# ==========================================

parametros = st.query_params

token_confirmacao = parametros.get("confirmar")
token_redefinicao = parametros.get("redefinir")


# ==========================================
# CONFIRMAÇÃO DE E-MAIL
# ==========================================

if token_confirmacao:

    sucesso, mensagem = confirmar_email_via_token(
        token_confirmacao
    )

    st.query_params.clear()

    if sucesso:
        st.success(mensagem)
    else:
        st.error(mensagem)

    st.info(
        "Você já pode acessar sua conta na aba Entrar."
    )

    st.stop()


# ==========================================
# REDEFINIÇÃO DE SENHA
# ==========================================

if token_redefinicao:

    st.markdown(
        '<div class="titulo">🔑 Redefinir senha</div>',
        unsafe_allow_html=True,
    )

    with st.form("form_redefinir_senha"):

        nova_senha = st.text_input(
            "Nova senha",
            type="password",
        )

        confirmar_nova_senha = st.text_input(
            "Confirme a nova senha",
            type="password",
        )

        st.caption(
            "A senha deve ter 8+ caracteres, "
            "com maiúscula, minúscula e número."
        )

        redefinir = st.form_submit_button(
            "Redefinir senha",
            type="primary",
        )

    if redefinir:

        sucesso, mensagem = redefinir_senha_via_token(
            token_redefinicao,
            nova_senha,
            confirmar_nova_senha,
        )

        if sucesso:

            st.query_params.clear()

            st.success(mensagem)

            st.info(
                "Sua senha foi redefinida. "
                "Volte à página inicial para entrar."
            )

        else:
            st.error(mensagem)

    st.stop()


# ==========================================
# VERIFICAR USUÁRIO LOGADO
# ==========================================

usuario = usuario_logado()


# ==========================================
# GATE DE LOGIN
# ==========================================

if usuario is None:

    pagina_login()

    st.stop()


# ==========================================
# CARREGAR SISTEMA PRINCIPAL
# Somente depois do login
# ==========================================

import main


# ==========================================
# NAVEGAÇÃO
# ==========================================

paginas = main.menu_para(usuario["tipo"])


# ==========================================
# PÁGINA INICIAL POR PERFIL
# ==========================================

if "pagina_atual" not in st.session_state:

    if usuario["tipo"] == main.TIPO_ADMIN:

        st.session_state.pagina_atual = " Administração"

    else:

        st.session_state.pagina_atual = paginas[0]


pagina = st.session_state.pagina_atual


# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================

main.render_pagina(
    pagina,
    usuario,
)
