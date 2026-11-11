import streamlit as st

from controllers.usuario_firebase_controller import (
    atualizar_usuario_admin,
    criar_usuario_admin,
    excluir_usuario_admin,
    listar_usuarios_admin,
)
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


PERFIS = [TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN]
STATUS = ["ativo", "inativo"]


def _mostrar_erro(erro):
    st.error(str(erro))


def renderizar_admin_usuarios(usuario_atual):
    st.markdown('<div class="titulo">Usuários Firebase</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo">Gerencie contas no Firebase Auth e Firestore.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Cadastrar usuário")

    with st.form("form_criar_usuario", clear_on_submit=True):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        perfil = st.selectbox("Perfil", PERFIS)
        status = st.selectbox("Status", STATUS)
        criar = st.form_submit_button("Criar usuário", type="primary")

    if criar:
        try:
            criar_usuario_admin(usuario_atual, nome, email, perfil, status)
            st.success("Usuário criado no Firebase.")
            st.rerun()
        except Exception as erro:
            _mostrar_erro(erro)

    st.divider()
    st.subheader("Contas cadastradas")

    try:
        usuarios = listar_usuarios_admin(usuario_atual)
    except Exception as erro:
        _mostrar_erro(erro)
        return

    if not usuarios:
        st.info("Ainda não há usuários no Firebase.")
        return

    for dados in usuarios:
        uid = dados["uid"]
        nome_atual = dados.get("nome", "")
        email_atual = dados.get("email", "")

        with st.expander(f"{nome_atual} — {email_atual}"):
            st.caption(f"UID: {uid}")

            with st.form(f"form_editar_{uid}"):
                nome = st.text_input(
                    "Nome",
                    value=nome_atual,
                    key=f"nome_{uid}",
                )
                email = st.text_input(
                    "E-mail",
                    value=email_atual,
                    key=f"email_{uid}",
                )

                perfil_atual = dados.get("perfil")
                indice_perfil = (
                    PERFIS.index(perfil_atual)
                    if perfil_atual in PERFIS
                    else 0
                )
                perfil = st.selectbox(
                    "Perfil",
                    PERFIS,
                    index=indice_perfil,
                    key=f"perfil_{uid}",
                )

                status_atual = dados.get("status", "ativo")
                indice_status = (
                    STATUS.index(status_atual)
                    if status_atual in STATUS
                    else 0
                )
                status = st.selectbox(
                    "Status",
                    STATUS,
                    index=indice_status,
                    key=f"status_{uid}",
                )

                salvar = st.form_submit_button("Salvar alterações")

            if salvar:
                try:
                    atualizar_usuario_admin(
                        usuario_atual, uid, nome, email, perfil, status
                    )
                    st.success("Usuário atualizado.")
                    st.rerun()
                except Exception as erro:
                    _mostrar_erro(erro)

            confirmar_exclusao = st.checkbox(
                "Confirmo que quero excluir esta conta.",
                key=f"confirmar_exclusao_{uid}",
            )
            if st.button(
                "Excluir usuário",
                key=f"excluir_{uid}",
                disabled=not confirmar_exclusao,
            ):
                try:
                    excluir_usuario_admin(usuario_atual, uid)
                    st.success("Usuário excluído do Firebase.")
                    st.rerun()
                except Exception as erro:
                    _mostrar_erro(erro)