import base64
import os

import streamlit as st
from utils.estado import fazer_login


def aplicar_fundo_login():
    diretorio_projeto = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    caminho_fundo = os.path.join(
        diretorio_projeto,
        "assets",
        "sala.png",
    )

    if not os.path.isfile(caminho_fundo):
        return

    with open(caminho_fundo, "rb") as arquivo:
        imagem_base64 = base64.b64encode(arquivo.read()).decode("ascii")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(8, 12, 22, 0.42),
                    rgba(8, 12, 22, 0.42)
                ),
                url("data:image/png;base64,{imagem_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: transparent !important;
        }}

        /* Barra superior transparente, com controles brancos */
        header[data-testid="stHeader"],
        [data-testid="stHeader"],
        [data-testid="stAppHeader"],
        [data-testid="stToolbar"] {{
            background: transparent !important;
            box-shadow: none !important;
            color: #ffffff !important;
        }}

        [data-testid="stHeader"] *,
        [data-testid="stToolbar"] * {{
            color: #ffffff !important;
            fill: #ffffff !important;
        }}

        /* Textos da tela em branco */
        .stApp [data-testid="stMarkdownContainer"] *,
        .stApp [data-testid="stWidgetLabel"] *,
        .stApp [data-testid="stExpander"] * {{
            color: #ffffff !important;
        }}

        /* Única palavra em azul */
        .stApp [data-testid="stMarkdownContainer"] .hero-highlight {{
            color: #60a5fa !important;
        }}

        /* Campos escuros translúcidos, com texto branco */
        .stApp [data-testid="stTextInput"] input {{
            color: #ffffff !important;
            background: rgba(15, 23, 42, 0.62) !important;
            border-color: rgba(255, 255, 255, 0.35) !important;
        }}

        .stApp [data-testid="stTextInput"] input::placeholder {{
            color: rgba(255, 255, 255, 0.72) !important;
        }}

        /* Botão de login */
        .stApp [data-testid="stFormSubmitButton"] button {{
            color: #ffffff !important;
            background-color: #ef4444 !important;
            border: none !important;
        }}

        .stApp [data-testid="stFormSubmitButton"] button * {{
            color: #ffffff !important;
        }}

        /* Cards translúcidos */
        .stApp .feature-card {{
            background: rgba(15, 23, 42, 0.48);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 8px;
            padding: 12px 6px;
            text-align: center;
        }}

        /* Formulário e contas de demonstração */
        .stApp [data-testid="stForm"],
        .stApp [data-testid="stExpander"] {{
            background: rgba(15, 23, 42, 0.42) !important;
            border: 1px solid rgba(255, 255, 255, 0.24) !important;
            border-radius: 10px !important;
        }}

        .stApp [data-testid="stAlert"] * {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def renderizar_categoria(icone, texto):
    st.markdown(
        f"""
        <div class="feature-card">
            <span style="font-size: 22px;">{icone}</span><br>
            <span>{texto}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pagina_login():
    aplicar_fundo_login()

    col_esquerda, col_direita = st.columns(
        [1.1, 1],
        gap="large",
    )

    # Painel esquerdo: apresentação
    with col_esquerda:
        st.markdown(
            '<div class="brand-title">Reserva de Salas</div>'
            '<div class="brand-subtitle">Sistema Acadêmico</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<h1 class="hero-title">'
            'Mais que salas,<br>'
            '<span class="hero-highlight">oportunidades.</span>'
            "</h1>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="hero-description">'
            "Reserve espaços da sua instituição de forma simples, "
            "rápida e segura. Aqui, cada sala é um passo para grandes ideias."
            "</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        cat1, cat2, cat3, cat4 = st.columns(4)

        with cat1:
            renderizar_categoria("💻", "Salas de Aula")

        with cat2:
            renderizar_categoria("🧪", "Laboratórios")

        with cat3:
            renderizar_categoria("🛠️", "Oficinas")

        with cat4:
            renderizar_categoria("🎭", "Auditórios")

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            '<p class="footer-text">'
            "TECNOLOGIA A SERVIÇO DA SUA JORNADA ACADÊMICA."
            "</p>",
            unsafe_allow_html=True,
        )

    # Painel direito: login
    with col_direita:
        st.markdown(
            '<div class="access-label">🔒 Acesso Restrito</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<h2 class="login-title">Bem-vindo de volta!</h2>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="login-description">'
            "Faça login para continuar com a reserva de salas."
            "</p>",
            unsafe_allow_html=True,
        )

        with st.form("form_login_moderno"):
            login_input = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário",
            )

            senha_input = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
            )

            entrar = st.form_submit_button(
                "Entrar",
                type="primary",
                use_container_width=True,
            )

        if entrar:
            sucesso, mensagem = fazer_login(login_input, senha_input)

            if sucesso:
                st.rerun()
            else:
                st.error(mensagem)

        with st.expander("Contas de demonstração"):
            st.caption("**Locatário:** usuário `marcos`")
            st.caption("**Proprietário:** usuário `ana`")