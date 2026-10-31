from controllers.auth_controller import validar_email
from models import usuario_firebase_model as model
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


PERFIS_VALIDOS = {
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
    TIPO_ADMIN,
}
STATUS_VALIDOS = {"ativo", "inativo"}


def _exigir_admin(usuario_atual):
    if not usuario_atual or usuario_atual.get("tipo") != TIPO_ADMIN:
        raise PermissionError("Apenas um administrador pode gerenciar usuários.")


def _validar_dados(nome, email, perfil, status):
    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    perfil = (perfil or "").strip()
    status = (status or "").strip().lower()

    if not nome:
        raise ValueError("Informe o nome.")

    if not validar_email(email):
        raise ValueError("Informe um e-mail válido.")

    if perfil not in PERFIS_VALIDOS:
        raise ValueError("Selecione um perfil válido.")

    if status not in STATUS_VALIDOS:
        raise ValueError("O status deve ser 'ativo' ou 'inativo'.")

    return nome, email, perfil, status


def _eh_proprio_usuario(usuario_atual, usuario_alvo):
    email_atual = (usuario_atual.get("email") or "").strip().lower()
    email_alvo = (usuario_alvo.get("email") or "").strip().lower()
    return bool(email_atual and email_atual == email_alvo)


def _proteger_ultimo_admin(uid, perfil_novo=None, status_novo=None):
    usuario = model.buscar_usuario(uid)

    if not usuario:
        raise ValueError("Usuário não encontrado.")

    continua_admin_ativo = (
        usuario.get("perfil") == TIPO_ADMIN
        and usuario.get("status") == "ativo"
        and (perfil_novo is None or perfil_novo != TIPO_ADMIN
             or status_novo == "inativo")
    )

    if not continua_admin_ativo:
        return

    admins_ativos = [
        item for item in model.listar_usuarios()
        if item.get("perfil") == TIPO_ADMIN
        and item.get("status") == "ativo"
    ]

    if len(admins_ativos) <= 1:
        raise ValueError("Não é possível remover ou desativar o último administrador ativo.")


def listar_usuarios_admin(usuario_atual):
    _exigir_admin(usuario_atual)
    return model.listar_usuarios()


def criar_usuario_admin(usuario_atual, nome, email, perfil, status="ativo"):
    _exigir_admin(usuario_atual)
    dados = _validar_dados(nome, email, perfil, status)
    return model.criar_usuario(*dados)


def atualizar_usuario_admin(
    usuario_atual, uid, nome, email, perfil, status
):
    _exigir_admin(usuario_atual)
    dados = _validar_dados(nome, email, perfil, status)

    usuario_alvo = model.buscar_usuario(uid)
    if not usuario_alvo:
        raise ValueError("Usuário não encontrado.")

    if _eh_proprio_usuario(usuario_atual, usuario_alvo):
        raise ValueError("Não é permitido alterar a própria conta por este painel.")

    _proteger_ultimo_admin(uid, perfil_novo=perfil, status_novo=status)
    model.atualizar_usuario(uid, *dados)


def excluir_usuario_admin(usuario_atual, uid):
    _exigir_admin(usuario_atual)

    usuario_alvo = model.buscar_usuario(uid)
    if not usuario_alvo:
        raise ValueError("Usuário não encontrado.")

    if _eh_proprio_usuario(usuario_atual, usuario_alvo):
        raise ValueError("Não é permitido excluir a própria conta.")

    _proteger_ultimo_admin(uid)
    model.excluir_usuario(uid)