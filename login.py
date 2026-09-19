import os
import streamlit as st
from estado import fazer_login


def pagina_login():
    # Centralização: Define a proporção das colunas para ajustar o formulário na tela
    col_esq, col_meio, col_dir = st.columns([1, 2, 1])

    with col_meio:
        # Cabeçalho flexível: Imagem no canto esquerdo e Título da aplicação
        col_img, col_txt = st.columns([0.25, 0.75], vertical_alignment="center")

        with col_img:
            # Obtém o caminho absoluto do diretório onde o login.py está localizado
            diretorio_base = os.path.dirname(os.path.abspath(__file__))
            
            # Caminho dinâmico para a imagem (procura em 'assets/logo.jpg' ou 'logo.jpg' na raiz)
            caminho_logo = os.path.join(diretorio_base, "assets", "logo.jpg")
            if not os.path.exists(caminho_logo):
                caminho_logo = os.path.join(diretorio_base, "logo.jpg")

            # Exibe a imagem se ela existir no projeto
            if os.path.exists(caminho_logo):
                st.image(caminho_logo, width=55)
            else:
                st.warning("Logo não encontrada")

        with col_txt:
            st.markdown(
                '<h2 style="margin: 0; font-size: 26px; font-weight: bold; color: #1e293b;">As Branquelas</h2>',
                unsafe_allow_html=True,
            )

        # Título secundário e descrição
        st.markdown(
            '<div class="titulo" style="margin-top: 12px;">🏢 Reserva de Salas</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="subtitulo">Entre com sua conta de Locatário ou Proprietário.</div>',
            unsafe_allow_html=True,
        )

        # Formulário de entrada de usuário e senha
        with st.form("form_login"):
            login_input = st.text_input("Usuário")
            senha_input = st.text_input("Senha", type="password")
            entrar = st.form_submit_button(
                "Entrar", type="primary", use_container_width=True
            )

        if entrar:
            if fazer_login(login_input, senha_input):
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

        # Bloco com credenciais de demonstração
        with st.expander("Contas de demonstração"):
            st.caption("**Locatário:** usuário `marcos` · senha `1234`")
            st.caption("**Proprietário:** usuário `ana` · senha `1234`")