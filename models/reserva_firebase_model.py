from datetime import datetime

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from utils.relogio import agora_local

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
LIMITE_FINALIDADE = 500

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
        data_reserva = datetime.strptime(data, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("A data deve estar no formato AAAA-MM-DD.")
    if data_reserva.isoformat() != data:
        raise ValueError("A data deve estar no formato AAAA-MM-DD.")

    try:
        inicio = datetime.strptime(hora_inicio, "%H:%M").time()
        fim = datetime.strptime(hora_fim, "%H:%M").time()
    except (TypeError, ValueError):
        raise ValueError("Os horários devem estar no formato HH:MM.")
    if inicio.strftime("%H:%M") != hora_inicio or fim.strftime("%H:%M") != hora_fim:
        raise ValueError("Os horários devem estar no formato HH:MM.")

    if fim <= inicio:
        raise ValueError("O horário final deve ser depois do inicial.")

    agora = agora_local().replace(tzinfo=None)

    if data_reserva < agora.date():
        raise ValueError("Não é possível reservar uma sala em uma data passada.")

    if data_reserva == agora.date() and inicio <= agora.time():
        raise ValueError(
            "Para hoje, o horário inicial deve ser posterior ao horário atual."
        )


def normalizar_finalidade(finalidade):
    """Campo opcional; preserva o conteúdo e remove apenas espaços externos."""
    if finalidade is None:
        return ""
    if not isinstance(finalidade, str):
        raise ValueError("A finalidade da reserva deve ser um texto.")
    finalidade = finalidade.strip()
    if len(finalidade) > LIMITE_FINALIDADE:
        raise ValueError(
            f"A finalidade da reserva deve ter no máximo {LIMITE_FINALIDADE} caracteres."
        )
    return finalidade


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
    finalidade="",
):
    _validar_data_horarios(data, hora_inicio, hora_fim)
    finalidade = normalizar_finalidade(finalidade)

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
        "finalidade": finalidade,
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

    db = obter_firestore()
    referencia = db.collection(COLECAO_RESERVAS).document()
    sala_ref = db.collection("salas").document(str(sala_id))

    @firestore.transactional
    def _criar(transaction):
        _validar_data_horarios(data, hora_inicio, hora_fim)
        sala_doc = sala_ref.get(transaction=transaction)
        if not sala_doc.exists:
            raise ValueError("Esta sala não está mais disponível.")
        sala_atual = sala_doc.to_dict() or {}
        pedidos = _reservas_da_sala_data(db, transaction, sala_id, data)
        for pedido in pedidos:
            if (
                pedido.get("status") in {PENDENTE, APROVADA}
                and pedido.get("solicitante_uid") == str(solicitante_uid)
                and pedido.get("hora_inicio") == hora_inicio
                and pedido.get("hora_fim") == hora_fim
            ):
                raise ValueError("Você já tem um pedido ativo para esta sala e período.")

        # Recalcula o alerta dentro da transação, usando os dados atuais.
        conflitos = [
            pedido["id"] for pedido in pedidos
            if pedido.get("status") in {PENDENTE, APROVADA}
            and _sobrepoe(pedido, hora_inicio, hora_fim)
        ]
        dados_atuais = {
            **dados,
            "sala_nome": sala_atual.get("nome") or dados["sala_nome"],
            "proprietario_login": sala_atual.get("proprietario", ""),
            "precisa_revisao_admin": bool(conflitos),
            "conflitos_reserva_ids": conflitos,
        }
        _coordenar_sala(transaction, sala_ref)
        transaction.set(referencia, dados_atuais)

    _criar(db.transaction())
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


def _reservas_da_sala_data(db, transaction, sala_id, data):
    consulta = (
        db.collection(COLECAO_RESERVAS)
        .where(filter=FieldFilter("sala_id", "==", str(sala_id)))
        .where(filter=FieldFilter("data", "==", data))
    )
    return [
        {**(documento.to_dict() or {}), "id": documento.id}
        for documento in transaction.get(consulta)
    ]


def _sobrepoe(reserva, inicio, fim):
    # Registros ativos malformados não podem liberar uma aprovação por engano.
    try:
        inicio_atual = datetime.strptime(reserva["hora_inicio"], "%H:%M").time()
        fim_atual = datetime.strptime(reserva["hora_fim"], "%H:%M").time()
        inicio_novo = datetime.strptime(inicio, "%H:%M").time()
        fim_novo = datetime.strptime(fim, "%H:%M").time()
    except (KeyError, TypeError, ValueError) as erro:
        raise ValueError("Há reserva ativa com horário inválido. Revise os dados da sala.") from erro
    if fim_atual <= inicio_atual:
        raise ValueError("Há reserva ativa com período inválido. Revise os dados da sala.")
    return inicio_novo < fim_atual and fim_novo > inicio_atual


def _coordenar_sala(transaction, sala_ref):
    # Todas as mutações de reservas escrevem no mesmo documento da sala.
    # Isso serializa também consultas que ainda não encontraram sobreposição.
    transaction.update(sala_ref, {"reservas_atualizadas_em": firestore.SERVER_TIMESTAMP})


def alterar_status_reserva(reserva_id, novo_status, ator_uid, solicitante_uid=None):
    if novo_status not in STATUS_RESERVA:
        raise ValueError("Status de reserva inválido.")
    if not ator_uid:
        raise ValueError("Não foi possível identificar quem alterou a reserva.")

    db = obter_firestore()
    referencia = db.collection(COLECAO_RESERVAS).document(str(reserva_id))

    @firestore.transactional
    def _atualizar(transaction):
        documento = referencia.get(transaction=transaction)
        if not documento.exists:
            raise ValueError("Reserva não encontrada.")
        dados = documento.to_dict() or {}
        status_atual = dados.get("status")
        if solicitante_uid is not None and dados.get("solicitante_uid") != solicitante_uid:
            raise PermissionError("Você só pode cancelar seus próprios pedidos.")
        if status_atual not in STATUS_RESERVA:
            raise ValueError("A reserva tem um status inválido.")
        if novo_status not in _TRANSICOES_PERMITIDAS[status_atual]:
            raise ValueError(f"Não é permitido mudar de {status_atual} para {novo_status}.")

        sala_ref = db.collection("salas").document(str(dados.get("sala_id")))
        sala_doc = sala_ref.get(transaction=transaction)

        if novo_status == APROVADA:
            if not sala_doc.exists:
                raise ValueError("Esta sala não está mais disponível.")
            _validar_data_horarios(dados.get("data"), dados.get("hora_inicio"), dados.get("hora_fim"))
            reservas = _reservas_da_sala_data(db, transaction, dados["sala_id"], dados["data"])
            if any(
                reserva["id"] != str(reserva_id)
                and reserva.get("status") == APROVADA
                and _sobrepoe(reserva, dados["hora_inicio"], dados["hora_fim"])
                for reserva in reservas
            ):
                raise ValueError("Já existe uma reserva aprovada que ocupa este horário.")

        # Todas as leituras precedem as escritas, como exige o Firestore.
        if sala_doc.exists:
            _coordenar_sala(transaction, sala_ref)
        transaction.update(referencia, {
            "status": novo_status,
            "atualizada_em": firestore.SERVER_TIMESTAMP,
            "decidida_por_uid": str(ator_uid),
        })

    _atualizar(db.transaction())
