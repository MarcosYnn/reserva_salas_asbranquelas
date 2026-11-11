import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv não instalado: use variáveis de ambiente do sistema

from utils.estado import (
    inicializar_estado, usuario_logado, fazer_logout,
    confirmar_email_via_token, redefinir_senha_via_token,
)
from utils.componentes import injetar_css
from views.login_view import pagina_login
import main


# ==========================================
# Configuração da página
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
# Streamlit não tem rotas de verdade — os links de confirmação e de
# redefinição de senha chegam como parâmetros na própria URL do app
# (?confirmar=TOKEN ou ?redefinir=TOKEN) e são tratados aqui, antes
# de qualquer outra coisa, tanto logado quanto deslogado.
# ==========================================

parametros = st.query_params
token_confirmacao = parametros.get("confirmar")
token_redefinicao = parametros.get("redefinir")

if token_confirmacao:
    sucesso, mensagem = confirmar_email_via_token(token_confirmacao)
    st.query_params.clear()

    if sucesso:
        st.success(mensagem)
    else:
        st.error(mensagem)

    st.info("Você já pode ir para a aba **Entrar** para acessar sua conta.")
    pagina_login()
    st.stop()

if token_redefinicao:
    st.markdown(
        '<div class="titulo">🔑 Redefinir senha</div>',
        unsafe_allow_html=True
    )

    with st.form("form_redefinir_senha"):
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar_nova_senha = st.text_input(
            "Confirme a nova senha",
            type="password"
        )

        st.caption(
            "A senha deve ter 8+ caracteres, com maiúscula, minúscula e número."
        )

        redefinir = st.form_submit_button(
            "Redefinir senha",
            type="primary"
        )

    if redefinir:
        sucesso, mensagem = redefinir_senha_via_token(
            token_redefinicao,
            nova_senha,
            confirmar_nova_senha
        )

        if sucesso:
            st.query_params.clear()
            st.success(mensagem)
            st.info(
                "Você já pode ir para a aba **Entrar** para acessar sua conta."
            )
            pagina_login()
        else:
            st.error(mensagem)

    st.stop()


usuario = usuario_logado()

# ==========================================
# GATE DE LOGIN
# Sem usuário logado, nem a sidebar nem o conteúdo aparecem.
# ==========================================

if usuario is None:
    pagina_login()
    st.stop()


# ==========================================
# SIDEBAR (só é montada com usuário autenticado)
# ==========================================

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


# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================

main.render_pagina(pagina, usuario)