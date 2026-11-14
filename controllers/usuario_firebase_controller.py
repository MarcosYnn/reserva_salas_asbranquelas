import re

from controllers.auth_controller import (
    validar_email,
    validar_senha_forte,
)
from models import usuario_firebase_model as model
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
STATUS_VALIDOS = {"ativo", "inativo"}
PADRAO_USUARIO = re.compile(r"^[a-z0-9._-]{3,30}$")


def _exigir_admin(usuario_atual):
    if not usuario_atual or usuario_atual.get("tipo") != TIPO_ADMIN:
        raise PermissionError(
            "Apenas um administrador pode gerenciar usuários."
        )


def _validar_dados(usuario, nome, email, perfil, status):
    usuario = (usuario or "").strip().lower()
    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    perfil = (perfil or "").strip()
    status = (status or "").strip().lower()

    if not PADRAO_USUARIO.fullmatch(usuario):
        raise ValueError(
            "O usuário deve ter de 3 a 30 caracteres: "
            "letras sem acento, números, ponto, hífen ou sublinhado."
        )
    if not nome:
        raise ValueError("Informe o nome.")
    if not validar_email(email):
        raise ValueError("Informe um e-mail válido.")
    if perfil not in PERFIS_VALIDOS:
        raise ValueError("Selecione um perfil válido.")
    if status not in STATUS_VALIDOS:
        raise ValueError("O status deve ser 'ativo' ou 'inativo'.")

    return usuario, nome, email, perfil, status


def _eh_proprio_usuario(usuario_atual, usuario_alvo):
    id_atual = usuario_atual.get("id")
    id_alvo = usuario_alvo.get("uid")
    if id_atual and id_alvo:
        return id_atual == id_alvo

    email_atual = (usuario_atual.get("email") or "").strip().lower()
    email_alvo = (usuario_alvo.get("email") or "").strip().lower()
    return bool(email_atual and email_atual == email_alvo)


def _proteger_ultimo_admin(uid, perfil_novo=None, status_novo=None):
    usuario = model.buscar_usuario(uid)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    esta_removendo_admin_ativo = (
        usuario.get("perfil") == TIPO_ADMIN
        and usuario.get("status") == "ativo"
        and (
            perfil_novo is None
            or perfil_novo != TIPO_ADMIN
            or status_novo == "inativo"
        )
    )
    if not esta_removendo_admin_ativo:
        return

    admins_ativos = [
        item
        for item in model.listar_usuarios()
        if item.get("perfil") == TIPO_ADMIN
        and item.get("status") == "ativo"
    ]
    if len(admins_ativos) <= 1:
        raise ValueError(
            "Não é possível remover ou desativar o último "
            "administrador ativo."
        )


def listar_usuarios_admin(usuario_atual):
    _exigir_admin(usuario_atual)
    return model.listar_usuarios()


def criar_usuario_admin(
    usuario_atual,
    nome,
    email,
    senha,
    confirmar_senha,
    perfil,
    status="ativo",
    usuario=None,
):
    _exigir_admin(usuario_atual)
    usuario, nome, email, perfil, status = _validar_dados(
        usuario,
        nome,
        email,
        perfil,
        status,
    )

    senha_ok, mensagem = validar_senha_forte(senha)
    if not senha_ok:
        raise ValueError(mensagem)
    if senha != confirmar_senha:
        raise ValueError("As senhas não coincidem.")

    return model.criar_usuario(
        usuario,
        nome,
        email,
        perfil,
        status,
        senha,
    )


def atualizar_usuario_admin(
    usuario_atual,
    uid,
    nome,
    email,
    perfil,
    status,
    nova_senha="",
    confirmar_nova_senha="",
    usuario=None,
):
    _exigir_admin(usuario_atual)

    usuario_alvo = model.buscar_usuario(uid)
    if not usuario_alvo:
        raise ValueError("Usuário não encontrado.")
    if _eh_proprio_usuario(usuario_atual, usuario_alvo):
        raise ValueError(
            "Não é permitido alterar a própria conta por este painel."
        )

    if usuario is None:
        usuario = usuario_alvo.get("usuario", "")

    usuario, nome, email, perfil, status = _validar_dados(
        usuario,
        nome,
        email,
        perfil,
        status,
    )

    if nova_senha or confirmar_nova_senha:
        senha_ok, mensagem = validar_senha_forte(nova_senha)
        if not senha_ok:
            raise ValueError(mensagem)
        if nova_senha != confirmar_nova_senha:
            raise ValueError("As senhas não coincidem.")

    _proteger_ultimo_admin(
        uid,
        perfil_novo=perfil,
        status_novo=status,
    )
    model.atualizar_usuario(
        uid,
        usuario,
        nome,
        email,
        perfil,
        status,
        senha=nova_senha or None,
    )


def excluir_usuario_admin(usuario_atual, uid):
    _exigir_admin(usuario_atual)

    usuario_alvo = model.buscar_usuario(uid)
    if not usuario_alvo:
        raise ValueError("Usuário não encontrado.")
    if _eh_proprio_usuario(usuario_atual, usuario_alvo):
        raise ValueError("Não é permitido excluir a própria conta.")

    _proteger_ultimo_admin(uid)
    model.excluir_usuario(uid)