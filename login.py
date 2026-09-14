import streamlit as st

from estado import fazer_login, cadastrar_usuario, solicitar_redefinicao_senha


def pagina_login():
    col_esq, col_meio, col_dir = st.columns([1, 1.4, 1])

    with col_meio:
        st.markdown('<div class="titulo">🏢 Reserva de Salas</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitulo">Entre com sua conta ou crie uma nova.</div>',
            unsafe_allow_html=True,
        )

        aba_entrar, aba_criar_conta, aba_recuperar = st.tabs(
            ["Entrar", "Criar conta", "Esqueci a senha"]
        )

        with aba_entrar:
            _formulario_login()

        with aba_criar_conta:
            _formulario_cadastro()

        with aba_recuperar:
            _formulario_recuperacao()


def _formulario_login():
    with st.form("form_login"):
        identificador = st.text_input("Usuário ou e-mail")
        senha_input = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    if entrar:
        sucesso, mensagem = fazer_login(identificador, senha_input)
        if sucesso:
            st.rerun()
        else:
            st.error(mensagem)

    with st.expander("Contas de demonstração"):
        st.caption("**Administrador:** `admin` · senha `Admin@123`")
        st.caption("**Locatário:** `marcos` · senha `Marcos@123`")
        st.caption("**Proprietário:** `ana` · senha `Ana@12345`")


def _formulario_cadastro():
    with st.form("form_cadastro"):
        nome_completo = st.text_input("Nome completo")
        nome_usuario = st.text_input("Nome de usuário")
        email = st.text_input("E-mail")
        tipo_conta = st.selectbox("Tipo de conta", ["Locatário", "Proprietário"])
        senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirme a senha", type="password")
        st.caption("A senha deve ter 8+ caracteres, com maiúscula, minúscula e número.")
        criar = st.form_submit_button("Criar conta", type="primary", use_container_width=True)

    if criar:
        sucesso, mensagem = cadastrar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            nome_completo=nome_completo,
            senha=senha,
            confirmar_senha=confirmar_senha,
            tipo=tipo_conta,
        )
        if sucesso:
            st.success(mensagem)
        else:
            st.error(mensagem)


def _formulario_recuperacao():
    st.caption("Informe o e-mail cadastrado para receber um link de redefinição de senha.")
    with st.form("form_recuperacao"):
        email = st.text_input("E-mail cadastrado")
        enviar = st.form_submit_button("Enviar link de redefinição", use_container_width=True)

    if enviar:
        sucesso, mensagem = solicitar_redefinicao_senha(email)
        if sucesso:
            st.success(mensagem)
        else:
            st.error(mensagem)
