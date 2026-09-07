import streamlit as st
from estado import fazer_login


def pagina_login():
    col_esq, col_meio, col_dir = st.columns([1, 1.4, 1])

    with col_meio:
        st.markdown('<div class="titulo">🏢 Reserva de Salas</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitulo">Entre com sua conta de Locatário ou Proprietário.</div>',
            unsafe_allow_html=True,
        )

        with st.form("form_login"):
            login_input = st.text_input("Usuário")
            senha_input = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)

        if entrar:
            if fazer_login(login_input, senha_input):
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

        with st.expander("Contas de demonstração"):
            st.caption("**Locatário:** usuário `marcos` · senha `1234`")
            st.caption("**Proprietário:** usuário `ana` · senha `1234`")
