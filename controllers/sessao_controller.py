import streamlit as st
from firebase_admin import auth

from models.firebase_client import obter_app_firebase
from models import usuario_firebase_model as usuario_model
from utils.sessao import limpar_dados_usuario


PERFIS_VALIDOS = {"Locatário", "Proprietário", "Administrador"}


def revalidar_usuario(usuario):
    """Reconsulta Auth e perfil; nunca autoriza pelo perfil antigo da sessão."""
    if not usuario or not usuario.get("id"):
        raise PermissionError("Faça login para continuar.")

    uid = usuario["id"]
    try:
        perfil = usuario_model.buscar_usuario(uid)
        conta = auth.get_user(uid, app=obter_app_firebase())
    except auth.UserNotFoundError:
        limpar_dados_usuario()
        raise PermissionError("Sua conta não está mais disponível. Faça login novamente.")
    except Exception as erro:
        # Falhar na consulta não deve liberar ações com permissões em cache.
        raise PermissionError("Não foi possível verificar seu acesso. Tente novamente.") from erro

    if (
        not perfil
        or perfil.get("uid") != uid
        or conta.uid != uid
        or conta.disabled
        or perfil.get("status") != "ativo"
        or perfil.get("perfil") not in PERFIS_VALIDOS
        or (perfil.get("email") or "").strip().lower()
        != (conta.email or "").strip().lower()
    ):
        limpar_dados_usuario()
        raise PermissionError("Seu acesso foi alterado ou bloqueado. Faça login novamente.")

    login = perfil.get("usuario") or ""
    novo_tipo = perfil["perfil"]
    if usuario.get("tipo") != novo_tipo or usuario.get("login") != login:
        limpar_dados_usuario()

    usuario.update(
        login=login,
        usuario=login,
        nome=perfil.get("nome") or login,
        email=perfil.get("email"),
        tipo=novo_tipo,
        eh_admin=novo_tipo == "Administrador",
    )
    # O dicionário em uso pelas páginas também passa a conter o perfil atual.
    st.session_state.usuario = usuario
    return usuario
