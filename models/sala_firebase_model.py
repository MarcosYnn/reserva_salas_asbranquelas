from uuid import uuid4

from models.firebase_client import obter_firestore


COLECAO_SALAS = "salas"

SALAS_DEMONSTRACAO = [
    {
        "id": 1,
        "nome": "Sala Executiva",
        "capacidade": 12,
        "localizacao": "2º andar",
        "proprietario": "ana",
        "projetor": True,
        "computador": False,
        "internet": True,
        "webcam": False,
        "quadro": False,
        "ar_condicionado": False,
    },
    {
        "id": 2,
        "nome": "Sala de Reunião 01",
        "capacidade": 8,
        "localizacao": "2º andar",
        "proprietario": "ana",
        "projetor": False,
        "computador": False,
        "internet": True,
        "webcam": False,
        "quadro": False,
        "ar_condicionado": False,
    },
    {
        "id": 3,
        "nome": "Sala de Reunião 02",
        "capacidade": 8,
        "localizacao": "2º andar",
        "proprietario": "ana",
        "projetor": False,
        "computador": False,
        "internet": True,
        "webcam": False,
        "quadro": False,
        "ar_condicionado": False,
    },
    {
        "id": 4,
        "nome": "Sala de Treinamento",
        "capacidade": 20,
        "localizacao": "3º andar",
        "proprietario": "ana",
        "projetor": True,
        "computador": False,
        "internet": True,
        "webcam": False,
        "quadro": False,
        "ar_condicionado": False,
    },
]


def garantir_salas_demonstracao():
    db = obter_firestore()
    referencia = db.collection(COLECAO_SALAS)

    if next(referencia.limit(1).stream(), None):
        return

    for sala in SALAS_DEMONSTRACAO:
        referencia.document(str(sala["id"])).set(sala)


def listar_salas():
    documentos = (
        obter_firestore()
        .collection(COLECAO_SALAS)
        .stream()
    )

    salas = []
    for documento in documentos:
        dados = documento.to_dict() or {}
        dados["id"] = dados.get("id", documento.id)
        dados.setdefault("proprietario", "ana")
        salas.append(dados)

    return sorted(
        salas,
        key=lambda sala: str(sala.get("id", "")),
        reverse=True,
    )


def criar_sala(
    nome,
    capacidade,
    localizacao,
    proprietario,
    recursos_marcados,
):
    nome = (nome or "").strip()
    localizacao = (localizacao or "").strip()
    proprietario = (proprietario or "").strip()

    if not nome:
        raise ValueError("Informe o nome da sala.")
    if int(capacidade) < 1:
        raise ValueError("A capacidade deve ser maior que zero.")

    recursos = set(recursos_marcados or [])
    sala_id = uuid4().hex

    dados = {
        "id": sala_id,
        "nome": nome,
        "capacidade": int(capacidade),
        "localizacao": localizacao,
        "proprietario": proprietario,
        "projetor": "projetor" in recursos,
        "computador": "computador" in recursos,
        "internet": "internet" in recursos,
        "webcam": "webcam" in recursos,
        "quadro": "quadro" in recursos,
        "ar_condicionado": "ar_condicionado" in recursos,
    }

    (
        obter_firestore()
        .collection(COLECAO_SALAS)
        .document(sala_id)
        .set(dados)
    )

    return dados


def excluir_sala(sala_id):
    referencia = (
        obter_firestore()
        .collection(COLECAO_SALAS)
        .document(str(sala_id))
    )

    if not referencia.get().exists:
        raise ValueError("Sala não encontrada no Firestore.")

    referencia.delete()