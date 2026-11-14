
import streamlit as st
from html import escape
from textwrap import dedent

from views.admin_usuarios_firebase import renderizar_admin_usuarios
from utils.estado import usuario_logado


# ==========================================
# MENU ADMINISTRATIVO
# ==========================================

def menu_administrativo():
    if "admin_pagina" not in st.session_state:
        st.session_state.admin_pagina = "Início"

    with st.container(key="admin_menu"):
        col1, col2, col3, col4 = st.columns(
            [1, 1, 1.5, 5],
            gap="small"
        )

        with col1:
            if st.button(
                "Início",
                key="menu_inicio",
                use_container_width=True
            ):
                st.session_state.admin_pagina = "Início"
                st.session_state.pop("admin_secao", None)
                st.rerun()

        with col2:
            if st.button(
                "Usuários",
                key="menu_usuarios",
                use_container_width=True
            ):
                st.session_state.admin_pagina = "Usuários"
                st.session_state.pop("admin_secao", None)
                st.rerun()

        with col3:
            if st.button(
                "Configurações",
                key="menu_configuracoes",
                use_container_width=True
            ):
                st.session_state.admin_pagina = "Configurações"
                st.session_state.pop("admin_secao", None)
                st.rerun()


# ==========================================
# ESTILOS DO PAINEL
# ==========================================

def estilos_admin():
    st.markdown("""
    <style>

    /* Fundo principal */
    [data-testid="stAppViewContainer"] {
        background: #f3f6fb;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 100%;
        padding: 1rem 1.5rem 3rem;
    }

    /* Menu administrativo */
    .st-key-admin_menu {
        background: #143864;
        padding: 10px 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .st-key-admin_menu button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #ffffff !important;
    }

    .st-key-admin_menu button p,
    .st-key-admin_menu button span,
    .st-key-admin_menu button div {
        color: #ffffff !important;
    }

    .st-key-admin_menu button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
    }

    .st-key-admin_menu button:focus {
        background: rgba(255, 255, 255, 0.18) !important;
        color: #ffffff !important;
    }

    .st-key-admin_menu button:hover p,
    .st-key-admin_menu button:focus p {
        color: #ffffff !important;
    }

    /* Cabeçalho */
    .admin-topo {
        background: #143864;
        color: #ffffff !important;
        padding: 16px 22px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
    }

    .admin-topo,
    .admin-topo * {
        color: #ffffff !important;
    }

    .admin-marca {
        font-size: 13px;
        font-weight: 700;
    }

    .admin-marca small {
        display: block;
        font-size: 9px;
        color: #b8cbe4 !important;
    }

    .admin-perfil {
        font-size: 12px;
        text-align: right;
    }

    .admin-perfil small {
        display: block;
        color: #cbdcf0 !important;
        margin-top: 3px;
    }

    /* Painel de boas-vindas */
    .admin-hero {
        background: linear-gradient(115deg, #153963, #2867ad);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 36px 30px;
        min-height: 230px;
        box-shadow: 0 6px 15px #17395c20;
    }

    .admin-hero,
    .admin-hero * {
        color: #ffffff !important;
    }

    .admin-hero small {
        color: #c3d8ef !important;
        font-size: 11px;
        letter-spacing: 1px;
    }

    .admin-hero h2 {
        color: #ffffff !important;
        font-size: 28px;
        margin: 14px 0;
        font-weight: 700;
    }

    .admin-hero p {
        color: #e2ecf8 !important;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Títulos das seções */
    .admin-titulo {
        font-size: 16px;
        font-weight: 700;
        color: #183b63 !important;
        margin-top: 22px;
    }

    .admin-subtitulo {
        font-size: 12px;
        color: #718096 !important;
        margin-bottom: 12px;
    }

    /* Cards */
    .admin-card {
        background: #ffffff;
        border: 1px solid #e3e9f2;
        border-radius: 12px;
        padding: 24px;
        min-height: 145px;
        box-shadow: 0 3px 10px #1b355010;
    }

    .admin-card h4 {
        color: #173c67 !important;
        font-size: 14px;
        margin: 12px 0 5px;
        font-weight: 700;
    }

    .admin-card p {
        color: #718096 !important;
        font-size: 12px;
        line-height: 1.5;
    }

    .admin-icone {
        display: inline-block;
        background: #edf4ff;
        border-radius: 8px;
        padding: 10px;
        font-size: 19px;
    }

    </style>
    """, unsafe_allow_html=True)


# ==========================================
# PAINEL ADMINISTRATIVO
# ==========================================

def mostrar_admin():
    estilos_admin()

    # Usuário autenticado
    usuario = usuario_logado()

    nome = escape(
        str(usuario.get("nome", "Administrador"))
        if usuario else "Administrador"
    )

    # Cabeçalho
        # Cabeçalho
    st.markdown(
        '<div class="admin-topo">'
        '<div class="admin-marca">'
        '▣ SISTEMA DE GESTÃO'
        '<small>REDE EDUCACIONAL</small>'
        '</div>'
        f'<div class="admin-perfil">{nome}'
        '<small>Administrador</small>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Menu superior
    menu_administrativo()

    pagina_atual = st.session_state.get(
        "admin_pagina", "Início"
    )

    # =============st.mar=========================
    # PÁGINA USUÁRIOS - FIREBASE
    # ======================================

    if pagina_atual == "Usuários":
        if usuario is None:
            st.error(
                "Sessão não encontrada. Faça login novamente."
            )
            return

        renderizar_admin_usuarios(usuario)
        return

    # ======================================
    # PÁGINA CONFIGURAÇÕES
    # ======================================

    if pagina_atual == "Configurações":
        st.title("⚙️ Configurações")
        st.info(
            "As configurações administrativas serão implementadas aqui."
        )
        return

    # ======================================
    # PÁGINA INÍCIO
    # ======================================

    st.markdown(
        '<div class="admin-hero">'
        '<small>PAINEL ADMINISTRATIVO</small>'
        '<h2>Bem-vindo ao Sistema de Agendamento</h2>'
        '<p>Olá! Estamos prontos para ajudar você a começar.</p>'
        '<p>Acesse as principais funções do sistema pelo menu acima.</p>'
        '</div>',
        unsafe_allow_html=True
    )
    # Botão começar
    if st.button(
        "Vamos começar",
        key="admin_comecar"
    ):
        st.session_state.admin_pagina = "Usuários"
        st.session_state.admin_secao = "usuarios"
        st.rerun()

    # ======================================
    # AÇÕES RÁPIDAS
    # ======================================

    st.markdown("""
    <div class="admin-titulo">
        Ações rápidas
    </div>

    <div class="admin-subtitulo">
        Escolha uma atividade para continuar
        no ambiente administrativo.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(
        [1, 1, 0.7],
        gap="medium"
    )

    # Card 1 - Permissões
    with col1:
        st.markdown("""
        <div class="admin-card">
            <span class="admin-icone">🛡️</span>
            <h4>Gerenciar permissões</h4>
            <p>
                Defina perfis e níveis de acesso dos usuários.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Gerenciar permissões",
            key="admin_permissoes"
        ):
            st.session_state.admin_pagina = "Usuários"
            st.session_state.admin_secao = "permissoes"
            st.rerun()

    # Card 2 - Consultar usuários
    with col2:
        st.markdown("""
        <div class="admin-card">
            <span class="admin-icone">👥</span>
            <h4>Consultar usuários</h4>
            <p>
                Localize os acessos já cadastrados no sistema.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Consultar usuários",
            key="admin_consultar"
        ):
            st.session_state.admin_pagina = "Usuários"
            st.session_state.admin_secao = "usuarios"
            st.rerun()

    # Card 3 - Cadastrar usuário
    with col3:
        st.markdown("""
        <div class="admin-card">
            <h4>Status inicial 🟢</h4>
            <p>
                O ambiente está pronto para receber
                novos registros.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Cadastrar usuário",
            key="admin_cadastrar"
        ):
            st.session_state.admin_pagina = "Usuários"
            st.session_state.admin_secao = "cadastro"
            st.rerun()
