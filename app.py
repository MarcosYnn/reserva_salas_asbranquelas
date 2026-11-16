from datetime import date
from html import escape

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from utils.estado import (
    fazer_logout,
    inicializar_estado,
    recarregar_salas,
    usuario_logado,
)
from utils.componentes import injetar_css, renderizar_cabecalho_pagina
from views.login_view import pagina_login
import main


st.set_page_config(
    page_title="Reserva de Salas",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

injetar_css()
inicializar_estado()
recarregar_salas()

usuario = usuario_logado()

if usuario is None:
    pagina_login()
    st.stop()


paginas = main.menu_para(usuario["tipo"])
if not paginas:
    st.error("Este perfil não possui páginas disponíveis.")
    st.stop()

rotulos = {
    "Dashboard": "Início",
    "Buscar Salas": "Buscar salas",
    "Minhas Reservas": "Minhas reservas",
    "Favoritos": "Favoritos",
    "Minhas Salas": "Minhas salas",
    "Pedidos de Reserva": "Pedidos de reserva",
    "Perfil": "Perfil",
    "Administração": "Administração",
}
icones = {
    "Dashboard": "⌂",
    "Buscar Salas": "▦",
    "Minhas Reservas": "▣",
    "Favoritos": "♡",
    "Minhas Salas": "▦",
    "Pedidos de Reserva": "◷",
    "Perfil": "◉",
    "Administração": "⚙",
}

if st.session_state.get("pagina_atual") not in paginas:
    st.session_state.pagina_atual = paginas[0]

with st.sidebar:
    st.markdown(
        '<div class="app-brand">▦ &nbsp; Reserva de Salas'
        '<small>Sistema Acadêmico</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="app-menu-label">Menu</div>', unsafe_allow_html=True)

    for chave_pagina in paginas:
        texto = f"{icones.get(chave_pagina, '•')}   {rotulos.get(chave_pagina, chave_pagina)}"
        ativo = st.session_state.pagina_atual == chave_pagina
        if st.button(
            texto,
            key=f"nav_{chave_pagina}",
            type="primary" if ativo else "secondary",
            use_container_width=True,
        ):
            st.session_state.pagina_atual = chave_pagina
            st.rerun()

    st.markdown('<div style="height: 1.5rem"></div>', unsafe_allow_html=True)
    nome_usuario = str(usuario.get("nome") or "Usuário")
    tipo_usuario = str(usuario.get("tipo") or "Conta")
    st.markdown(
        '<div class="app-user">'
        f'{escape(nome_usuario)}'
        f'<small>Conta de {escape(tipo_usuario)}</small>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("↪   Sair", key="sair_app", use_container_width=True):
        fazer_logout()
        st.rerun()

pagina = st.session_state.pagina_atual
rotulo_pagina = rotulos.get(pagina, pagina)
data_atual = date.today()
meses = (
    "jan", "fev", "mar", "abr", "mai", "jun",
    "jul", "ago", "set", "out", "nov", "dez",
)
subtitulo = f"{data_atual.day} {meses[data_atual.month - 1]} {data_atual.year} · Sistema Acadêmico"
renderizar_cabecalho_pagina(rotulo_pagina, subtitulo)
main.render_pagina(pagina, usuario)
