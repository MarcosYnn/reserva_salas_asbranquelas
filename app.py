from pathlib import Path
import base64
import streamlit as st
from views.admin_view import mostrar_admin

st.set_page_config(
    page_title="Reserva de Salas",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_IMAGEM = BASE_DIR / "assets" / "sala_aula.jpg"

# Função para carregar a imagem

def carregar_imagem(caminho):
    if not caminho.is_file():
        st.warning("Imagem de fundo não encontrada.")
        return None

    try:
        with open(caminho, "rb") as arquivo:
            imagem = arquivo.read()

        if not imagem:
            st.warning(
                f"A imagem de fundo está vazia: {caminho.name}. "
                "Salve a foto nessa pasta, substituindo o arquivo vazio."
            )
            return None

        return base64.b64encode(imagem).decode("utf-8")

    except OSError as erro:
        st.error(f"Erro ao carregar imagem: {erro}")
        return None


if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""


def aplicar_estilos_login():
    imagem = carregar_imagem(CAMINHO_IMAGEM)

    camada = (
        "linear-gradient(90deg, "
        "rgba(9,13,25,0.82), "
        "rgba(12,20,40,0.65))"
    )

    if imagem:
        fundo = (
            f'{camada}, '
            f'url("data:image/jpeg;base64,{imagem}")'
        )
    else:
        fundo = "linear-gradient(135deg, #121722, #29334b)"

    css = """
    <style>
    #MainMenu, footer, [data-testid="stHeader"] {display:none !important;}
    [data-testid="stAppViewContainer"] {background:#f7f9fc;}
    [data-testid="stMainBlockContainer"] {
        padding:0 !important; max-width:100% !important;
    }
    .st-key-login_shell > div[data-testid="stVerticalBlock"] {gap:0 !important;}
    .st-key-login_shell [data-testid="stHorizontalBlock"] {
        gap:0 !important; align-items:stretch !important; min-height:100vh;
    }
    .st-key-login_shell [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        background-image:__FUNDO__;
        background-size:cover; background-position:center;
        padding:30px 28px !important; min-height:100vh;
    }
    .st-key-login_shell [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        background:#f7f9fc; padding:24px 28px !important;
        min-height:100vh;
    }
    .st-key-login_shell [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlock"] {
        min-height:calc(100vh - 48px); justify-content:center;
    }
    .marca {font-size:14px;font-weight:700;color:#fff;line-height:1.3;}
    .marca small {display:block;color:#6ca3ff;font-size:10px;letter-spacing:1.4px;}
    
.hero {
    margin-top: clamp(100px, 23vh, 240px);
    position: relative;
    z-index: 2;
}

.chamada {
    color: #ffffff !important;
    font-size: clamp(30px, 3vw, 44px);
    font-weight: 750;
    line-height: 1.2;
    max-width: 620px;
}

.chamada .destaque {
    display: block;
    color: #3675ff !important;
}

.descricao {
    margin-top: 18px;
    color: #dce5f4;
    font-size: 14px;
    line-height: 1.65;
    max-width: 410px;
}

.categorias {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 28px;
}

.categoria {
     border: 1px solid #ffffff30;
    background: #ffffff12;
    color: white;
    border-radius: 10px;
    padding: 13px 11px;
    font-size: 11px;
    text-align: center;
    min-width: 82px;
}

.rodape-esquerdo {
    color: #9ab0d0;
    font-size: 9px;
    letter-spacing: 1px;
    margin-top: clamp(60px, 18vh, 200px);
}

    .acesso-restrito {text-align:right;color:#64748b;font-size:11px;}
    .st-key-login_shell [data-testid="stForm"] {
        background:#fff;border:1px solid #dfe7f1;border-radius:14px;
        padding:24px;max-width:430px;width:100%;margin:0 auto !important;
        box-shadow:0 3px 10px #15233b10;
    }
    .login-titulo {color:#111827;font-size:22px;font-weight:700;margin:12px 0 3px;}
    .login-subtitulo {color:#64748b;font-size:12px;margin-bottom:16px;}
    .st-key-login_shell [data-testid="stFormSubmitButton"] button {
        background:#2864f0 !important;color:white !important;border:0 !important;
        border-radius:9px !important;min-height:42px;
    }
    .st-key-login_shell [data-testid="stFormSubmitButton"] button:hover {background:#174fd0 !important;}
    .st-key-login_shell [data-testid="stExpander"] {max-width:430px;margin:0 auto;}
    @media(max-width:750px) {
        .st-key-login_shell [data-testid="stHorizontalBlock"] {flex-direction:column !important;}
        .st-key-login_shell [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {min-height:450px;}
        .st-key-login_shell [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {min-height:560px;}
        .hero {margin-top:75px;}
        .rodape-esquerdo {margin-top:65px;}
    }
    </style>
    """
    st.markdown(css.replace("__FUNDO__", fundo), unsafe_allow_html=True)


def tela_login():
    aplicar_estilos_login()
    with st.container(key="login_shell"):
        esquerda, direita = st.columns([1.4, 1], gap=None)
       
        
    
        with esquerda:
            st.markdown(
                '<div class="marca">▦ &nbsp; RESERVA DE SALAS'
                '<small>GESTÃO INTELIGENTE</small></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="hero">'
                '<div class="chamada">'
                'Simplifique a gestão e '
                '<span class="destaque">reserva de espaços.</span>'
                '</div>'
                '<div class="descricao">'
                'Organize reuniões, aulas e eventos com total '
                'controle de horários e disponibilidade em tempo real.'
                '</div>'
                '<div class="categorias">'
                '<div class="categoria">🏫<br>Salas de Aula</div>'
                '<div class="categoria">🧪<br>Laboratórios</div>'
                '<div class="categoria">🔧<br>Oficinas</div>'
                '<div class="categoria">👥<br>Auditórios</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="rodape-esquerdo">'
                '━ &nbsp; TECNOLOGIA A SERVIÇO DA SUA JORNADA ACADÊMICA.'
                '</div>',
                unsafe_allow_html=True
            )


        with direita:
            st.markdown('<div class="acesso-restrito">🔒 Acesso Restrito</div>', unsafe_allow_html=True)
            with st.form("form_login_visual"):
                st.markdown("""
                <div style="display:inline-block;background:#eff6ff;color:#2563eb;border-radius:10px;padding:10px;font-size:22px;">♙</div>
                <div class="login-titulo">Bem-vindo de volta!</div>
                <div class="login-subtitulo">Faça login para continuar com a reserva de salas.</div>
                """, unsafe_allow_html=True)
                usuario = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_usuario")
                senha = st.text_input("Senha", placeholder="Digite sua senha", type="password", key="login_senha")
                entrar = st.form_submit_button("➜ Entrar", use_container_width=True)

            if entrar:
                if not usuario.strip() or not senha:
                    st.warning("Preencha o usuário e a senha.")
                elif usuario.strip() == "admin" and senha == "1234":
                    # Credenciais apenas para teste; substituir por autenticação segura antes de publicar.
                    st.session_state.logado = True
                    st.session_state.usuario = usuario.strip()
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

            with st.expander("🔒 Esqueceu sua senha?"):
                st.info("Entre em contato com o administrador do sistema para recuperar sua senha.")



def sistema():
    # Verifica se o usuário está autenticado
    if not st.session_state.get("logado", False):
        st.warning("Você precisa fazer login.")
        return

    # Exibe a segunda página do Canva
    mostrar_admin()

    st.divider()

    # Encerrar sessão
    if st.button("🚪 Sair da conta", key="sair_admin"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.session_state.pop("admin_secao", None)
        st.rerun()


if st.session_state.logado:
    sistema()
else:
    tela_login()
