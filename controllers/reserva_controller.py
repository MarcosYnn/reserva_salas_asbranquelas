from datetime import datetime

from models import reserva_firebase_model as reserva_model
from models import sala_firebase_model as sala_model
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


PRIORIDADE_NORMAL = 1
PRIORIDADE_AULA_PRATICA = 2
PRIORIDADE_EVENTO = 3


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


def classificar_prioridade(
    necessita_equipamentos,
    evento_institucional=False,
):
    if evento_institucional:
        return PRIORIDADE_EVENTO

    if necessita_equipamentos:
        return PRIORIDADE_AULA_PRATICA

    return PRIORIDADE_NORMAL


def converter_horario(horario):
    """Converte 'HH:MM - HH:MM' em horários comparáveis."""
    try:
        inicio_txt, fim_txt = horario.split(" - ")
        inicio = datetime.strptime(inicio_txt.strip(), "%H:%M").time()
        fim = datetime.strptime(fim_txt.strip(), "%H:%M").time()
    except (ValueError, AttributeError):
        raise ValueError(
            "Horário inválido. Use o formato HH:MM - HH:MM."
        )

    if inicio >= fim:
        raise ValueError("O horário final deve ser posterior ao inicial.")

    return inicio, fim


def horarios_se_sobrepoem(horario1, horario2):
    inicio1, fim1 = converter_horario(horario1)
    inicio2, fim2 = converter_horario(horario2)

    return inicio1 < fim2 and fim1 > inicio2


def _intervalo_da_reserva(reserva):
    """Lê os horários separados do Firestore ou o campo antigo do PR."""
    inicio = reserva.get("hora_inicio")
    fim = reserva.get("hora_fim")

    if inicio and fim:
        return f"{inicio} - {fim}"

    return reserva.get("horario", "")


def buscar_conflitos(
    reservas,
    sala_id,
    data,
    hora_inicio,
    hora_fim,
    reserva_id=None,
):
    horario_pedido = f"{hora_inicio} - {hora_fim}"
    conflitos = []

    status_ativos = {
        reserva_model.PENDENTE,
        reserva_model.APROVADA,
    }

    for reserva in reservas:
        if reserva.get("status") not in status_ativos:
            continue

        if (
            reserva_id is not None
            and str(reserva.get("id")) == str(reserva_id)
        ):
            continue

        mesma_sala = str(reserva.get("sala_id")) == str(sala_id)
        mesma_data = reserva.get("data") == data

        if not mesma_sala or not mesma_data:
            continue

        horario_existente = _intervalo_da_reserva(reserva)
        if not horario_existente:
            continue

        try:
            sobrepoe = horarios_se_sobrepoem(
                horario_existente,
                horario_pedido,
            )
        except ValueError:
            # Ignora registros antigos com horário em formato inválido.
            continue

        if sobrepoe:
            conflitos.append(reserva)

    return conflitos


def avaliar_solicitacao(
    reservas,
    sala_id,
    data,
    hora_inicio,
    hora_fim,
    necessita_equipamentos=False,
    evento_institucional=False,
):
    conflitos = buscar_conflitos(
        reservas=reservas,
        sala_id=sala_id,
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
    )

    return {
        "prioridade": classificar_prioridade(
            necessita_equipamentos=necessita_equipamentos,
            evento_institucional=evento_institucional,
        ),
        "conflitos": conflitos,
        "precisa_revisao_admin": bool(conflitos),
    }


def criar_pedido_reserva(
    usuario_atual,
    sala,
    data,
    hora_inicio,
    hora_fim,
    necessita_equipamentos=False,
    evento_institucional=False,
):
    _exigir_perfil(usuario_atual, {TIPO_LOCATARIO})

    if not sala:
        raise ValueError("Selecione uma sala válida.")

    reservas = reserva_model.listar_reservas()

    avaliacao = avaliar_solicitacao(
        reservas=reservas,
        sala_id=sala["id"],
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        necessita_equipamentos=necessita_equipamentos,
        evento_institucional=evento_institucional,
    )

    ids_conflitos = [
        reserva.get("id")
        for reserva in avaliacao["conflitos"]
        if reserva.get("id")
    ]

    return reserva_model.criar_reserva(
        sala_id=sala["id"],
        sala_nome=sala["nome"],
        proprietario_login=sala.get("proprietario", ""),
        solicitante_uid=_uid(usuario_atual),
        solicitante_nome=usuario_atual.get("nome", ""),
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        prioridade=avaliacao["prioridade"],
        necessita_equipamentos=necessita_equipamentos,
        evento_institucional=evento_institucional,
        precisa_revisao_admin=avaliacao["precisa_revisao_admin"],
        conflitos_reserva_ids=ids_conflitos,
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

    # Os pedidos acompanham a sala se ela mudar de proprietário.
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