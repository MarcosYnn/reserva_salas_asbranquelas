from controllers.sessao_controller import revalidar_usuario
from models import favorito_firebase_model as model


def _exigir_locatario(usuario):
    revalidar_usuario(usuario)
    if usuario.get("tipo") != "Locatário":
        raise PermissionError("Seu perfil não pode gerenciar favoritos.")


def listar_favoritos(usuario):
    _exigir_locatario(usuario)
    return model.listar_favoritos(usuario["id"])


def definir_favorito(usuario, sala_id, favorito):
    _exigir_locatario(usuario)
    model.definir_favorito(usuario["id"], sala_id, favorito)
    return model.listar_favoritos(usuario["id"])
