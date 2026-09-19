import streamlit as st
from estado import fazer_login


def pagina_login():
    # Ajusta as proporções das colunas para centralizar melhor o conteúdo na tela
    col_esq, col_meio, col_dir = st.columns([1, 2, 1])

    with col_meio:
        # Cabeçalho com Logo "As Branquelas" e Imagem alinhados no canto superior esquerdo
        col_img, col_txt = st.columns([0.2, 0.8], vertical_alignment="center")
        
        with col_img:
           
            st.image("logo.png", width=50)
            
        with col_txt:
            st.markdown(
                '<h2 style="margin: 0; font-size: 24px; font-weight: bold; color: #1e293b;">As Branquelas</h2>', 
                unsafe_allow_html=True
            )

        st.markdown('<div class="titulo" style="margin-top: 10px;">🏢 Reserva de Salas</div>', unsafe_allow_html=True)
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