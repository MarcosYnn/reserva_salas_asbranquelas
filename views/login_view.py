import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def pagina_login():
    # Carrega a imagem da sala como background em base64
    img_base64 = get_base64_of_bin_file('assets/sala.png')
    
    bg_style = f'url("data:image/png;base64,{img_base64}")' if img_base64 else "none"

    # Estilização CSS completa
    custom_css = f"""
    <style>
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu, header, footer {{
        visibility: hidden;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, rgba(8, 12, 22, 0.88) 0%, rgba(13, 22, 38, 0.82) 100%), {bg_style};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }}

    /* Ajuste de espaçamento geral */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }}

    /* Header e Título */
    .brand-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0px;
        line-height: 1.2;
    }}
    .brand-subtitle {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #4B7BEC;
        letter-spacing: 1px;
        margin-top: 2px;
        margin-bottom: 2.5rem;
    }}

    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
        margin-bottom: 0.5rem;
    }}
    .hero-title-highlight {{
        color: #3B82F6;
    }}

    .hero-desc {{
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
        max-width: 480px;
        margin-bottom: 2rem;
    }}

    /* Container dos Cards Translúcidos */
    .card-grid {{
        display: flex;
        gap: 0.8rem;
        margin-bottom: 2.5rem;
    }}

    .category-card {{
        flex: 1;
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 1rem 0.5rem;
        text-align: center;
    }}

    .category-icon {{
        font-size: 1.4rem;
        margin-bottom: 0.4rem;
        display: block;
    }}

    .category-text {{
        font-size: 0.75rem;
        font-weight: 500;
        color: #E2E8F0;
    }}

    /* Rodapé */
    .footer-text {{
        font-size: 0.7rem;
        color: #64748B;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border-left: 2px solid #3B82F6;
        padding-left: 8px;
    }}

    /* Estilização da caixa de Login */
    div[data-testid="stForm"] {{
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
    }}

    .stTextInput > div > div {{
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 8px !important;
    }}

    .stTextInput label {{
        color: #CBD5E1 !important;
    }}

    div[data-testid="stForm"] button[type="submit"] {{
        background-color: #EF4444 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Colunas principais
    col_left, col_right = st.columns([1.2, 0.8], gap="large")

    with col_left:
        # String HTML em uma linha/sem quebras brutas para evitar o erro de código do Streamlit
        html_conteudo = """<div class="brand-title">🏛️ Reserva de Salas</div><div class="brand-subtitle">SISTEMA ACADÂMICO</div><h1 class="hero-title">Mais que salas,<br><span class="hero-title-highlight">oportunidades.</span></h1><p class="hero-desc">Reserve espaços da sua instituição de forma simples, rápida e segura. Aqui, cada sala é um passo para grandes ideias.</p><div class="card-grid"><div class="category-card"><span class="category-icon">🖥️</span><span class="category-text">Salas de Aula</span></div><div class="category-card"><span class="category-icon">🧪</span><span class="category-text">Laboratórios</span></div><div class="category-card"><span class="category-icon">🔧</span><span class="category-text">Oficinas</span></div><div class="category-card"><span class="category-icon">👥</span><span class="category-text">Auditórios</span></div></div><div class="footer-text">TECNOLOGIA A SERVIÇO DA SUA JORNADA ACADÊMICA.</div>"""
        
        st.markdown(html_conteudo, unsafe_allow_html=True)

    with col_right:
        with st.form("login_form"):
            st.markdown("<h2 style='color: white; font-size: 1.8rem; margin-bottom: 0.2rem;'>Bem-vindo de volta!</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 1.5rem;'>Faça login para continuar com a reserva de salas.</p>", unsafe_allow_html=True)
            
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            btn_login = st.form_submit_button("Entrar", use_container_width=True)
            
            if btn_login:
                if usuario and senha:
                    st.success("Login realizado com sucesso!")
                else:
                    st.error("Preencha todos os campos.")