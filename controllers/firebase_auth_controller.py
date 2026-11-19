import requests
import streamlit as st
from firebase_admin import auth as firebase_auth

from models import usuario_firebase_model as usuario_model
from models.firebase_client import obter_app_firebase
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


PERFIS_VALIDOS = {
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
}

URL_LOGIN_FIREBASE = (
    "https://identitytoolkit.googleapis.com/v1/"
    "accounts:signInWithPassword"
)


def autenticar_usuario_firebase(usuario, senha):
    usuario = (usuario or "").strip().lower()
    senha = senha or ""

    if not usuario or not senha:
        return False, "Informe o usuário e a senha."

    try:
        perfil_usuario = usuario_model.buscar_usuario_por_usuario(usuario)
    except Exception as erro:
        return False, (
            f"Falha ao consultar o Firestore: "
            f"{type(erro).__name__}: {erro}"
        )

    if not perfil_usuario:
        return False, "Usuário ou senha inválidos."

    if (perfil_usuario.get("status") or "").lower() != "ativo":
        return False, "Esta conta está inativa."

    tipo = perfil_usuario.get("perfil")
    if tipo not in PERFIS_VALIDOS:
        return False, "O perfil desta conta não é válido."

    email = (perfil_usuario.get("email") or "").strip().lower()
    if not email:
        return False, "A conta não possui e-mail cadastrado no Firestore."

    try:
        api_key = st.secrets["firebase"]["web_api_key"]
    except Exception:
        return False, (
            "A configuração firebase.web_api_key não foi encontrada "
            "nos secrets do Streamlit."
        )

    try:
        resposta = requests.post(
            URL_LOGIN_FIREBASE,
            params={"key": api_key},
            json={
                "email": email,
                "password": senha,
                "returnSecureToken": True,
            },
            timeout=15,
        )
    except requests.RequestException as erro:
        return False, (
            f"Falha de conexão com Firebase Auth: "
            f"{type(erro).__name__}"
        )

    try:
        dados_resposta = resposta.json()
    except ValueError:
        dados_resposta = {}

    if resposta.status_code != 200:
        erro = dados_resposta.get("error", {}).get(
            "message",
            "ERRO_SEM_CODIGO",
        )

        if erro in {
            "EMAIL_NOT_FOUND",
            "INVALID_PASSWORD",
            "INVALID_LOGIN_CREDENTIALS",
            "INVALID_EMAIL",
        }:
            return False, "Usuário ou senha inválidos."

        if erro == "USER_DISABLED":
            return False, "Esta conta está desativada no Firebase Auth."

        if erro == "API_KEY_INVALID":
            return False, "Firebase Auth: API_KEY_INVALID"

        if erro == "OPERATION_NOT_ALLOWED":
            return False, "Firebase Auth: OPERATION_NOT_ALLOWED"

        if erro == "TOO_MANY_ATTEMPTS_TRY_LATER":
            return False, "Muitas tentativas. Aguarde e tente novamente."

        return False, f"Firebase Auth retornou: {erro}"

    uid = dados_resposta.get("localId")
    token = dados_resposta.get("idToken")

    if not uid or not token:
        return False, "O Firebase não retornou UID ou token."

    try:
        app = obter_app_firebase()
        token_verificado = firebase_auth.verify_id_token(token, app=app)

        if token_verificado.get("uid") != uid:
            return False, "O UID do token não corresponde à conta."
    except Exception as erro:
        return False, (
            f"Falha ao validar o token: {type(erro).__name__}: {erro}"
        )

    nome = perfil_usuario.get("nome") or usuario

    st.session_state.usuario = {
        "id": uid,
        "login": usuario,
        "usuario": usuario,
        "email": email,
        "nome": nome,
        "tipo": tipo,
        "eh_admin": tipo == TIPO_ADMIN,
    }

    return True, "Login efetuado com sucesso."