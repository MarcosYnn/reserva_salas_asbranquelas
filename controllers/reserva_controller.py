from models import reserva_firebase_model as reserva_model
from models import sala_firebase_model as sala_model
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


def _exigir_perfil(usuario, perfis_permitidos):
    if not usuario:
        raise PermissionError("É necessário estar autenticado.")

    if usuario.get("tipo") not in perfis_permitidos:
        raise PermissionError("Seu perfil não tem permissão para esta ação.")


def _uid(usuario):
    uid = usuario.get("id")
    if not uid:
        raise ValueError("Não foi possível identificar sua conta.")
    return uid


def _login(usuario):
    return (
        usuario.get("login")
        or usuario.get("usuario")
        or ""
    ).strip().lower()


def criar_pedido_reserva(
    usuario_atual,
    sala,
    data,
    hora_inicio,
    hora_fim,
):
    _exigir_perfil(usuario_atual, {TIPO_LOCATARIO})

    if not sala:
        raise ValueError("Selecione uma sala válida.")

    return reserva_model.criar_reserva(
        sala_id=sala["id"],
        sala_nome=sala["nome"],
        proprietario_login=sala.get("proprietario", ""),
        solicitante_uid=_uid(usuario_atual),
        solicitante_nome=usuario_atual.get("nome", ""),
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
    )


def listar_reservas_usuario(usuario_atual):
    _exigir_perfil(
        usuario_atual,
        {TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN},
    )

    reservas = reserva_model.listar_reservas()

    if usuario_atual["tipo"] == TIPO_ADMIN:
        return reservas

    if usuario_atual["tipo"] == TIPO_LOCATARIO:
        uid = _uid(usuario_atual)
        return [
            reserva
            for reserva in reservas
            if reserva.get("solicitante_uid") == uid
        ]

    # Usa o proprietário atual cadastrado na sala. Assim, os pedidos
    # antigos também acompanham a sala se ela mudar de proprietário.
    login_proprietario = _login(usuario_atual)
    salas_por_id = {
        str(sala.get("id")): sala
        for sala in sala_model.listar_salas()
    }

    reservas_do_proprietario = []

    for reserva in reservas:
        sala = salas_por_id.get(str(reserva.get("sala_id")))
        if not sala:
            continue

        proprietario_da_sala = (
            sala.get("proprietario") or ""
        ).strip().lower()

        if proprietario_da_sala == login_proprietario:
            reservas_do_proprietario.append(reserva)

    return reservas_do_proprietario


def listar_reservas_ativas_para_busca(usuario_atual):
    _exigir_perfil(usuario_atual, {TIPO_LOCATARIO})

    status_que_ocupam_horario = {
        reserva_model.PENDENTE,
        reserva_model.APROVADA,
    }

    return [
        reserva
        for reserva in reserva_model.listar_reservas()
        if reserva.get("status") in status_que_ocupam_horario
    ]


def alterar_status_reserva_admin(
    usuario_atual,
    reserva_id,
    novo_status,
):
    _exigir_perfil(usuario_atual, {TIPO_ADMIN})

    if novo_status not in {
        reserva_model.APROVADA,
        reserva_model.RECUSADA,
        reserva_model.CANCELADA,
    }:
        raise ValueError(
            "O administrador pode aprovar, recusar ou cancelar a reserva."
        )

    reserva_model.alterar_status_reserva(
        reserva_id=reserva_id,
        novo_status=novo_status,
        ator_uid=_uid(usuario_atual),
    )


def cancelar_reserva_locatario(usuario_atual, reserva_id):
    _exigir_perfil(usuario_atual, {TIPO_LOCATARIO})

    reserva = reserva_model.buscar_reserva(reserva_id)
    if not reserva:
        raise ValueError("Reserva não encontrada.")

    if reserva.get("solicitante_uid") != _uid(usuario_atual):
        raise PermissionError("Você só pode cancelar seus próprios pedidos.")

    reserva_model.alterar_status_reserva(
        reserva_id=reserva_id,
        novo_status=reserva_model.CANCELADA,
        ator_uid=_uid(usuario_atual),
    )