from models.firebase_client import obter_firestore


def _colecao(uid):
    if not uid:
        raise ValueError("Conta não identificada.")
    return obter_firestore().collection("usuarios").document(str(uid)).collection("favoritos")


def listar_favoritos(uid):
    return {documento.id for documento in _colecao(uid).stream()}


def definir_favorito(uid, sala_id, favorito):
    sala_id = str(sala_id)
    if not sala_id or "/" in sala_id:
        raise ValueError("Sala inválida.")
    referencia = _colecao(uid).document(sala_id)
    if favorito:
        if not obter_firestore().collection("salas").document(sala_id).get().exists:
            raise ValueError("Esta sala não está mais disponível.")
        referencia.set({"sala_id": sala_id})
    else:
        referencia.delete()
