
import streamlit as st
st.set_page_config(
    page_title="Escritório Virtual",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)
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
    /* Menu lateral do protótipo */
[data-testid="stSidebar"] {
    background-color: #0b1020 !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #c6d2e8;
}

[data-testid="stSidebar"] button {
    border-radius: 8px;
}

[data-testid="stSidebar"] button:hover {
    background-color: #2563eb !important;
}

[data-testid="stSidebar"] button:hover * {
    color: #ffffff !important;
}

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

/* Posiciona o botão Vamos começar sobre o banner */
div.st-key-admin_comecar {
    position: relative !important;
    transform: translateY(-35px);
    margin-left: 20px;
    margin-bottom: -15px;
    z-index: 2;
}
}
}

div.st-key-admin_comecar button[kind="primary"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #153963 !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

div.st-key-admin_comecar button[kind="primary"]:hover {
    background: #dbeafe !important;
    color: #153963 !important;
}
}

.st-key-admin_comecar button:hover {
    background-color: #dbeafe !important;
    color: #153963 !important;
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
        background: #dbeafe;
        border-radius: 8px;
        padding: 10px;
        font-size: 19px;
    }
   
   
    /* Indicadores da Visão geral */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 8px;
}

div[data-testid="stMetricLabel"] p {
    color: #64748b !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

div[data-testid="stMetricValue"] {
    color: #173c67 !important;
    font-weight: 700 !important;
}

/* Botões do menu superior */
.admin-nav button,
.admin-nav button *,
.admin-menu button,
.admin-menu button * {
    color: #153963 !important;
}
/* Corrige os botões do menu superior */
div.st-key-menu_inicio button,
div.st-key-menu_usuarios button,
div.st-key-menu_configuracoes button {
    background-color: #ffffff !important;
    color: #153963 !important;
    border: 1px solid #dbe5f2 !important;
}

div.st-key-menu_inicio button *,
div.st-key-menu_usuarios button *,
div.st-key-menu_configuracoes button * {
    color: #153963 !important;
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
    key="admin_comecar",
    type="secondary"
):
        st.session_state.admin_pagina = "Usuários"
        st.session_state.admin_secao = "usuarios"
        st.rerun()

    # ======================================
    # INDICADORES DO DASHBOARD
    # ======================================

    from utils.estado import carregar_salas, listar_usuarios_admin

    total_salas = len(carregar_salas())
    total_usuarios = len(listar_usuarios_admin())

    reservas = st.session_state.get("reservas", [])

    total_reservas = len(reservas)

    # Ainda precisamos confirmar como o status
    # das reservas é representado no projeto.
    reservas_pendentes = sum(
    1 for reserva in reservas
    if reserva.get("status") == "Pendente"
)

    st.markdown("### 📊 Visão geral")
    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        with st.container(border=True):
            st.metric("🏢 Total de salas", total_salas)

    with col2:
        with st.container(border=True):
            st.metric("📅 Reservas na sessão", total_reservas)

    with col3:
        with st.container(border=True):
            st.metric("👥 Usuários cadastrados", total_usuarios)

    with col4:
        with st.container(border=True):
            st.metric("⏳ Reservas pendentes", reservas_pendentes)
        
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




     # ======================================
    # RESERVAS RECENTES E SALAS MAIS RESERVADAS
    # ======================================

    from datetime import datetime
    from collections import Counter

    reservas = st.session_state.get("reservas", [])
    salas = st.session_state.get("salas", [])

    # Organizar reservas por data
    reservas_recentes = sorted(
        reservas,
        key=lambda reserva: datetime.strptime(
            reserva["data"], "%d/%m/%Y"
        ),
        reverse=True
    )[:5]

    # Contar reservas de cada sala
    contagem = Counter(
        reserva["sala_id"]
        for reserva in reservas
        if reserva.get("sala_id") is not None
    )

    nomes_salas = {
        sala["id"]: sala["nome"]
        for sala in salas
    }

    dados_salas = [
        {
            "Sala": nomes_salas.get(sala_id, f"Sala {sala_id}"),
            "Total de reservas": quantidade
        }
        for sala_id, quantidade in contagem.most_common(5)
    ]

    # Criar duas colunas
    coluna_reservas, coluna_salas = st.columns(
        [1.7, 1],
        gap="medium"
    )

    # Coluna esquerda — Reservas recentes
    with coluna_reservas:
        st.markdown("### 📅 Reservas recentes")

        if reservas_recentes:
            dados_tabela = []

            for reserva in reservas_recentes:
                dados_tabela.append({
                    "Sala": nomes_salas.get(
                        reserva["sala_id"],
                        f"Sala {reserva['sala_id']}"
                    ),
                    "Cliente": reserva["cliente"],
                    "Data": reserva["data"],
                    "Horário": reserva["horario"],
                    "Status": reserva["status"]
                })

            st.dataframe(
                dados_tabela,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhuma reserva encontrada.")

    # Coluna direita — Salas mais reservadas
    with coluna_salas:
        st.markdown("### 🏢 Salas mais reservadas")

        if dados_salas:
            st.dataframe(
                dados_salas,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Ainda não existem reservas para exibir.")
        
        