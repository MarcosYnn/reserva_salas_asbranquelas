import json

import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore


@st.cache_resource
def obter_app_firebase():
    configuracao = st.secrets["firebase"]
    dados_conta = json.loads(configuracao["service_account_json"])

    project_id = configuracao["project_id"]
    if dados_conta.get("project_id") != project_id:
        raise ValueError(
            "O Project ID do secrets.toml não corresponde à conta de serviço."
        )

    try:
        return firebase_admin.get_app()
    except ValueError:
        credencial = credentials.Certificate(dados_conta)
        return firebase_admin.initialize_app(credencial)


@st.cache_resource
def obter_firestore():
    app = obter_app_firebase()
    return firestore.client(app=app)