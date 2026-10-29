from pathlib import Path
import base64
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_IMAGEM = BASE_DIR / "assets" / "sala_aula.jpg"

# =====================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# =====================================================

st.set_page_config(
    page_title="Reserva de Salas",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_IMAGEM = BASE_DIR / "assets" / "sala_aula.jpg"


# =====================================================
# ESTADO DA SESSÃO
# =====================================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""


# =====================================================
# CARREGAR IMAGEM DE FUNDO
# =====================================================

def carregar_imagem(caminho):
    if not caminho.exists():
        return None

    try:
        return base64.b64encode(
            caminho.read_bytes()
        ).decode("utf-8")
    except OSError:
        return None


# =====================================================
# TELA DE LOGIN
# =====================================================

def tela_login():
    imagem = carregar_imagem(CAMINHO_IMAGEM)

    if imagem:
        fundo_esquerdo = (
    'linear-gradient(90deg, '
    'rgba(10,14,24,0.65), '
    'rgba(10,14,24,0.55)), '
    f'url("data:image/jpeg;base64,{imagem}")'
)
        
    else:
        fundo_esquerdo = (
            'linear-gradient(135deg, #10131d, #29334a)'
        )

css = """
   css = """
<style>

.chamada {{
    color: #ffffff !important;
    font-size: clamp(30px, 3vw, 42px);
    line-height: 1.2;
    font-weight: 750;
}}

.chamada .destaque {{
    color: #3478ff !important;
}}

</style>
"""

st.markdown(css, unsafe_allow_html=True)
    /* Remover espaçamento superior */
[data-testid="stAppViewContainer"] .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

/* Remover espaços acima dos painéis */
[data-testid="stVerticalBlock"] {
    gap: 0;
}

/* Centralizar conteúdo do painel direito */
div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:last-child {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 100vh;
}

/* Ajustar cartão de login */
[data-testid="stForm"] {
    margin: 0 auto !important;
    max-width: 430px;
    width: 100%;
}

/* Botão Entrar azul */
[data-testid="stFormSubmitButton"] button {
    background-color: #2864f0 !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
}

[data-testid="stFormSubmitButton"] button:hover {
    background-color: #174fd0 !important;
    color: white !important;
}
    <style>
    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="stAppViewContainer"] {
        background: #f7f9fc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        min-height: 100vh;
        align-items: stretch;
    }

    div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:first-child {
        background-image: __FUNDO__;
background-size: cover;
background-position: center;
background-repeat: no-repeat;
min-height: 100vh;
padding: 30px 35px !important;
    }

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:last-of-type {
        background: #f7f9fc;
        padding: 24px 30px !important;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .marca {
        color: white;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .marca small {
        display: block;
        color: #60a5fa;
        font-size: 9px;
        letter-spacing: 2px;
    }

    .chamada {
        font-size: clamp(28px, 3vw, 42px);
        line-height: 1.2;
        font-weight: 750;
        margin-top: 22vh;
        margin-bottom: 14px;
    }

    .destaque {
        color: #3478ff;
    }

    .descricao {
        max-width: 400px;
        color: #ffffff;
        font-weight: 400;
        line-height: 1.6;
        font-size: 14px;
        opacity: 0.9;
    }

    .acesso-restrito {
        color: #64748b;
        font-size: 11px;
        text-align: right;
        width: 100%;
        max-width: 430px;
        margin-bottom: 8px;
    }

    [data-testid="stForm"] {
        background: white;
        border: 1px solid #e0e7f0;
        border-radius: 14px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        max-width: 430px;
        width: 100%;
        box-sizing: border-box;
        margin-bottom: 10px;
    }

    [data-testid="stForm"] label {
        color: #20314d;
        font-size: 12px;
    }

    [data-testid="stForm"] input {
        border-radius: 9px;
    }

    [data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background: #2864f0;
        color: white;
        border-radius: 9px;
        min-height: 42px;
        border: none;
    }

    [data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background: #174fd0;
        color: white;
    }
    
    div.esqueci-senha {
        max-width: 430px;
        width: 100%;
    }
    </style>
    """


    css = css.replace("__FUNDO__", fundo_esquerdo)
    st.markdown(css, unsafe_allow_html=True)

    esquerda, direita = st.columns([1.2, 1])

    with esquerda:
        st.markdown(
            """
            <div class="marca">
                RESERVA DE SALAS <small>GESTÃO INTELIGENTE</small>
            </div>
            <div class="chamada">
                Simplifique a gestão e <span class="destaque">reserva de espaços</span>.
            </div>
            <div class="descricao">
                Organize reuniões, aulas e eventos com total controle de horários e disponibilidade em tempo real.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with direita:
        st.markdown(
            '<div class="acesso-restrito">🔒 Acesso Restrito</div>',
            unsafe_allow_html=True,
        )

        with st.form("form_login_visual"):
            st.markdown(
                """
                <div style="background:#eff6ff; color:#2563eb; border-radius:10px; padding:10px; display:inline-block; font-size:22px;">
                    ♙
                </div>
                <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: #0f172a;">Bem-vindo de volta!</div>
                <div style="font-size: 13px; color: #64748b; margin-bottom: 15px;">Faça login para continuar com a reserva de salas.</div>
                """,
                unsafe_allow_html=True,
            )

            usuario = st.text_input(
                "Usuário", placeholder="Digite seu usuário", key="login_usuario"
            )
            senha = st.text_input(
                "Senha", placeholder="Digite sua senha", type="password", key="login_senha"
            )
            entrar = st.form_submit_button("➜ Entrar", use_container_width=True)

        if entrar:
            if not usuario.strip() or not senha:
                st.warning("Preencha o usuário e a senha.")
            elif usuario.strip() == "admin" and senha == "1234":
                st.session_state.logado = True
                st.session_state.usuario = usuario.strip()
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

        st.markdown('<div class="esqueci-senha">', unsafe_allow_html=True)
        with st.expander("🔒 Esqueceu sua senha?"):
            st.info("Entre em contato com o administrador do sistema para recuperar sua senha.")
        st.markdown('</div>', unsafe_allow_html=True)
        

# =====================================================
# SISTEMA APÓS O LOGIN
# =====================================================

def sistema():
    st.title("🏢 Escritório Virtual")
    st.write(f"Bem-vindo(a), {st.session_state.usuario}!")
    st.caption("Selecione uma opção para continuar.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Dashboard")
        if st.button("Abrir Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")

        st.subheader("🏢 Salas")
        if st.button("Gerenciar Salas", use_container_width=True):
            st.switch_page("pages/2_Salas.py")

    with col2:
        st.subheader("📅 Reservas")
        if st.button("Gerenciar Reservas", use_container_width=True):
            st.switch_page("pages/3_Reservas.py")

        st.subheader("👥 Usuários")
        if st.button("Gerenciar Usuários", use_container_width=True):
            st.switch_page("pages/4_Usuarios.py")

    st.divider()

    if st.button("🚪 Sair da conta"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.rerun()


# =====================================================
# EXECUÇÃO PRINCIPAL
# =====================================================

if st.session_state.logado:
    sistema()
else:
    tela_login()