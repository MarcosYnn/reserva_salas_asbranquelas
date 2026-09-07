import streamlit as st

from estado import inicializar_estado, usuario_logado, fazer_logout
from componentes import injetar_css
from login import pagina_login
import main


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
    st.markdown("## 🏢 Reserva de Salas")
    st.divider()

    st.markdown(f"### 👤 {usuario['nome']}")
    st.caption(f"Conta de {usuario['tipo']}")

    st.divider()
    st.markdown("### Menu")

    pagina = st.radio(
        "Navegação",
        main.menu_para(usuario["tipo"]),
        label_visibility="collapsed",
    )

    st.divider()
    if st.button("🚪 Sair"):
        fazer_logout()
        st.rerun()


# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================

main.render_pagina(pagina, usuario)
