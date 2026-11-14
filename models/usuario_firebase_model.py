import re

from firebase_admin import auth

from models.firebase_client import obter_app_firebase, obter_firestore


COLECAO_USUARIOS = "usuarios"
STATUS_VALIDOS = {"ativo", "inativo"}
PADRAO_USUARIO = re.compile(r"^[a-z0-9._-]{3,30}$")


def _normalizar_usuario(usuario):
    return (usuario or "").strip().lower()


def _usuario_do_perfil(dados):
    """
    Devolve o usuário salvo no perfil.

    Para perfis antigos que ainda não têm o campo "usuario",
    usa a parte do e-mail anterior ao @ como usuário temporário.
    Exemplo: souza@teste.com -> souza
    """
    usuario = dados.get("usuario")
    if usuario:
        return _normalizar_usuario(usuario)

    email = (dados.get("email") or "").strip().lower()
    return email.split("@", 1)[0] if "@" in email else ""


def _validar_campos(usuario, nome, email, perfil, status):
    usuario = _normalizar_usuario(usuario)
    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    perfil = (perfil or "").strip()
    status = (status or "").strip().lower()

    if not usuario:
        raise ValueError("Informe o nome de usuário.")
    if not PADRAO_USUARIO.fullmatch(usuario):
        raise ValueError(
            "O usuário deve ter de 3 a 30 caracteres: "
            "letras sem acento, números, ponto, hífen ou sublinhado."
        )
    if not nome or not email or not perfil:
        raise ValueError("Nome, e-mail e perfil são obrigatórios.")
    if status not in STATUS_VALIDOS:
        raise ValueError("Status deve ser 'ativo' ou 'inativo'.")

    return usuario, nome, email, perfil, status


def listar_usuarios():
    db = obter_firestore()
    usuarios = []

    for documento in db.collection(COLECAO_USUARIOS).stream():
        dados = documento.to_dict() or {}
        dados["uid"] = documento.id
        dados["usuario"] = _usuario_do_perfil(dados)
        usuarios.append(dados)

    return sorted(
        usuarios,
        key=lambda dados: (dados.get("nome") or "").casefold(),
    )


def buscar_usuario_por_usuario(usuario):
    usuario_procurado = _normalizar_usuario(usuario)
    if not usuario_procurado:
        return None

    encontrados = [
        dados
        for dados in listar_usuarios()
        if _usuario_do_perfil(dados) == usuario_procurado
    ]

    # Se houver nomes repetidos, não escolhe uma conta por engano.
    return encontrados[0] if len(encontrados) == 1 else None


def _validar_usuario_disponivel(usuario, exceto_uid=None):
    usuario = _normalizar_usuario(usuario)

    for existente in listar_usuarios():
        if existente.get("uid") == exceto_uid:
            continue

        if _usuario_do_perfil(existente) == usuario:
            raise ValueError("Este nome de usuário já está cadastrado.")


def criar_usuario(
    usuario,
    nome,
    email,
    perfil,
    status="ativo",
    senha=None,
):
    usuario, nome, email, perfil, status = _validar_campos(
        usuario,
        nome,
        email,
        perfil,
        status,
    )

    if not senha or len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres.")

    _validar_usuario_disponivel(usuario)

    app = obter_app_firebase()
    db = obter_firestore()

    conta = auth.create_user(
        email=email,
        password=senha,
        display_name=nome,
        disabled=(status == "inativo"),
        app=app,
    )

    dados = {
        "usuario": usuario,
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "status": status,
    }

    try:
        db.collection(COLECAO_USUARIOS).document(conta.uid).set(dados)
    except Exception:
        auth.delete_user(conta.uid, app=app)
        raise

    return conta.uid


def buscar_usuario(uid):
    documento = (
        obter_firestore()
        .collection(COLECAO_USUARIOS)
        .document(uid)
        .get()
    )

    if not documento.exists:
        return None

    dados = documento.to_dict() or {}
    dados["uid"] = documento.id
    dados["usuario"] = _usuario_do_perfil(dados)
    return dados


def atualizar_usuario(
    uid,
    usuario,
    nome,
    email,
    perfil,
    status,
    senha=None,
):
    usuario, nome, email, perfil, status = _validar_campos(
        usuario,
        nome,
        email,
        perfil,
        status,
    )

    if senha and len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres.")

    app = obter_app_firebase()
    db = obter_firestore()
    referencia = db.collection(COLECAO_USUARIOS).document(uid)
    documento = referencia.get()

    if not documento.exists:
        raise ValueError("Usuário não encontrado no Firestore.")

    _validar_usuario_disponivel(usuario, exceto_uid=uid)

    dados_antigos = documento.to_dict() or {}
    conta_antiga = auth.get_user(uid, app=app)
    email_alterado = email != conta_antiga.email

    dados_novos = {
        "usuario": usuario,
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "status": status,
    }

    # A senha fica somente no Firebase Authentication.
    referencia.set(dados_novos)

    try:
        opcoes = {
            "email": email,
            "display_name": nome,
            "disabled": (status == "inativo"),
            "email_verified": (
                False if email_alterado else conta_antiga.email_verified
            ),
            "app": app,
        }

        if senha:
            opcoes["password"] = senha

        auth.update_user(uid, **opcoes)

    except Exception:
        referencia.set(dados_antigos)
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
    referencia.delete()

    try:
        auth.delete_user(uid, app=app)
    except Exception:
        referencia.set(dados_antigos)
        raise