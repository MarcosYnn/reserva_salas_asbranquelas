from firebase_admin import auth

from models.firebase_client import obter_app_firebase, obter_firestore


COLECAO_USUARIOS = "usuarios"
STATUS_VALIDOS = {"ativo", "inativo"}


def _validar_campos(nome, email, perfil, status):
    nome = nome.strip()
    email = email.strip().lower()
    perfil = perfil.strip()
    status = status.strip().lower()

    if not nome or not email or not perfil:
        raise ValueError("Nome, e-mail e perfil são obrigatórios.")

    if status not in STATUS_VALIDOS:
        raise ValueError("Status deve ser 'ativo' ou 'inativo'.")

    return nome, email, perfil, status


def criar_usuario(nome, email, perfil, status="ativo"):
    nome, email, perfil, status = _validar_campos(
        nome, email, perfil, status
    )
    app = obter_app_firebase()
    db = obter_firestore()

    conta = auth.create_user(
        email=email,
        display_name=nome,
        disabled=(status == "inativo"),
        app=app,
    )

    dados = {
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "status": status,
    }

    try:
        db.collection(COLECAO_USUARIOS).document(conta.uid).set(dados)
    except Exception:
        # Evita deixar uma conta Auth sem o perfil correspondente.
        auth.delete_user(conta.uid, app=app)
        raise

    return conta.uid


def listar_usuarios():
    db = obter_firestore()
    usuarios = []

    for documento in db.collection(COLECAO_USUARIOS).stream():
        usuario = documento.to_dict() or {}
        usuario["uid"] = documento.id
        usuarios.append(usuario)

    return sorted(
        usuarios,
        key=lambda usuario: usuario.get("nome", "").casefold(),
    )


def buscar_usuario(uid):
    documento = (
        obter_firestore()
        .collection(COLECAO_USUARIOS)
        .document(uid)
        .get()
    )

    if not documento.exists:
        return None

    usuario = documento.to_dict() or {}
    usuario["uid"] = documento.id
    return usuario


def atualizar_usuario(uid, nome, email, perfil, status):
    nome, email, perfil, status = _validar_campos(
        nome, email, perfil, status
    )
    app = obter_app_firebase()
    db = obter_firestore()
    referencia = db.collection(COLECAO_USUARIOS).document(uid)
    documento = referencia.get()

    if not documento.exists:
        raise ValueError("Usuário não encontrado no Firestore.")

    dados_antigos = documento.to_dict() or {}
    conta_antiga = auth.get_user(uid, app=app)

    dados_novos = {
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "status": status,
    }

    email_alterado = email != conta_antiga.email

    # Atualiza Auth primeiro e restaura os dados antigos se o Firestore falhar.
    auth.update_user(
        uid,
        email=email,
        display_name=nome,
        disabled=(status == "inativo"),
        email_verified=False if email_alterado else conta_antiga.email_verified,
        app=app,
    )

    try:
        referencia.set(dados_novos)
    except Exception:
        auth.update_user(
            uid,
            email=conta_antiga.email,
            display_name=conta_antiga.display_name,
            disabled=conta_antiga.disabled,
            email_verified=conta_antiga.email_verified,
            app=app,
        )
        raise


def excluir_usuario(uid):
    app = obter_app_firebase()
    referencia = (
        obter_firestore()
        .collection(COLECAO_USUARIOS)
        .document(uid)
    )
    documento = referencia.get()

    if not documento.exists:
        raise ValueError("Usuário não encontrado no Firestore.")

    dados_antigos = documento.to_dict() or {}
    conta = auth.get_user(uid, app=app)

    # Se a exclusão no Auth falhar, restaura o perfil do Firestore.
    referencia.delete()
    try:
        auth.delete_user(uid, app=app)
    except Exception:
        referencia.set(dados_antigos)
        raise