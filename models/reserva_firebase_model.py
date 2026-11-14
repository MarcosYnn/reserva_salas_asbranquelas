from datetime import datetime

from google.cloud import firestore

from models.firebase_client import obter_firestore


COLECAO_RESERVAS = "reservas"

PENDENTE = "Pendente"
APROVADA = "Aprovada"
RECUSADA = "Recusada"
CANCELADA = "Cancelada"

STATUS_RESERVA = {
    PENDENTE,
    APROVADA,
    RECUSADA,
    CANCELADA,
}

PRIORIDADES_RESERVA = {1, 2, 3}

# Uma reserva pendente pode receber uma decisão ou ser cancelada.
# Uma aprovada pode ser cancelada. Recusada e cancelada são finais.
_TRANSICOES_PERMITIDAS = {
    PENDENTE: {APROVADA, RECUSADA, CANCELADA},
    APROVADA: {CANCELADA},
    RECUSADA: set(),
    CANCELADA: set(),
}


def _validar_data_horarios(data, hora_inicio, hora_fim):
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("A data deve estar no formato AAAA-MM-DD.")

    try:
        inicio = datetime.strptime(hora_inicio, "%H:%M")
        fim = datetime.strptime(hora_fim, "%H:%M")
    except (TypeError, ValueError):
        raise ValueError("Os horários devem estar no formato HH:MM.")

    if fim <= inicio:
        raise ValueError("O horário final deve ser depois do inicial.")


def criar_reserva(
    sala_id,
    sala_nome,
    proprietario_login,
    solicitante_uid,
    solicitante_nome,
    data,
    hora_inicio,
    hora_fim,
    prioridade=1,
    necessita_equipamentos=False,
    evento_institucional=False,
    precisa_revisao_admin=False,
    conflitos_reserva_ids=None,
):
    _validar_data_horarios(data, hora_inicio, hora_fim)

    campos_obrigatorios = {
        "sala_id": sala_id,
        "sala_nome": sala_nome,
        "solicitante_uid": solicitante_uid,
        "solicitante_nome": solicitante_nome,
    }
    if any(
        not str(valor or "").strip()
        for valor in campos_obrigatorios.values()
    ):
        raise ValueError("Faltam dados da sala ou do solicitante.")

    if prioridade not in PRIORIDADES_RESERVA:
        raise ValueError("A prioridade da reserva é inválida.")

    ids_conflitos = [
        str(reserva_id)
        for reserva_id in (conflitos_reserva_ids or [])
        if reserva_id
    ]

    dados = {
        "sala_id": str(sala_id),
        "sala_nome": str(sala_nome).strip(),
        "proprietario_login": str(
            proprietario_login or ""
        ).strip().lower(),
        "solicitante_uid": str(solicitante_uid).strip(),
        "solicitante_nome": str(solicitante_nome).strip(),
        "data": data,
        "hora_inicio": hora_inicio,
        "hora_fim": hora_fim,
        "status": PENDENTE,
        "prioridade": prioridade,
        "necessita_equipamentos": bool(necessita_equipamentos),
        "evento_institucional": bool(evento_institucional),
        "precisa_revisao_admin": bool(precisa_revisao_admin),
        "conflitos_reserva_ids": ids_conflitos,
        "criada_em": firestore.SERVER_TIMESTAMP,
        "atualizada_em": firestore.SERVER_TIMESTAMP,
        "decidida_por_uid": None,
    }

    referencia = obter_firestore().collection(
        COLECAO_RESERVAS
    ).document()
    referencia.set(dados)

    return referencia.id


def listar_reservas():
    documentos = (
        obter_firestore()
        .collection(COLECAO_RESERVAS)
        .stream()
    )

    reservas = []
    for documento in documentos:
        dados = documento.to_dict() or {}
        dados["id"] = documento.id
        reservas.append(dados)

    return sorted(
        reservas,
        key=lambda reserva: (
            reserva.get("data", ""),
            reserva.get("hora_inicio", ""),
        ),
        reverse=True,
    )


def buscar_reserva(reserva_id):
    documento = (
        obter_firestore()
        .collection(COLECAO_RESERVAS)
        .document(str(reserva_id))
        .get()
    )

    if not documento.exists:
        return None

    dados = documento.to_dict() or {}
    dados["id"] = documento.id
    return dados


def alterar_status_reserva(reserva_id, novo_status, ator_uid):
    if novo_status not in STATUS_RESERVA:
        raise ValueError("Status de reserva inválido.")

    if not ator_uid:
        raise ValueError(
            "Não foi possível identificar quem alterou a reserva."
        )

    db = obter_firestore()
    referencia = (
        db.collection(COLECAO_RESERVAS)
        .document(str(reserva_id))
    )
    transacao = db.transaction()

    @firestore.transactional
    def _atualizar(transaction):
        documento = referencia.get(transaction=transaction)

        if not documento.exists:
            raise ValueError("Reserva não encontrada.")

        dados = documento.to_dict() or {}
        status_atual = dados.get("status")

        if status_atual not in STATUS_RESERVA:
            raise ValueError("A reserva tem um status inválido.")

        if novo_status not in _TRANSICOES_PERMITIDAS[status_atual]:
            raise ValueError(
                f"Não é permitido mudar de {status_atual} "
                f"para {novo_status}."
            )

        transaction.update(
            referencia,
            {
                "status": novo_status,
                "atualizada_em": firestore.SERVER_TIMESTAMP,
                "decidida_por_uid": str(ator_uid),
            },
        )

    _atualizar(transacao)