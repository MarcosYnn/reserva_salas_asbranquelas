from models import reserva_firebase_model as reserva_model
from models import sala_firebase_model as sala_model
from utils.estado import (
    TIPO_ADMIN,
    TIPO_PROPRIETARIO,
    recarregar_salas,
)


def _login_usuario(usuario):
    return (
        usuario.get("login")
        or usuario.get("usuario")
        or ""
    ).strip().lower()


def _buscar_sala(sala_id):
    sala = next(
        (
            sala
            for sala in sala_model.listar_salas()
            if str(sala.get("id")) == str(sala_id)
        ),
        None,
    )

    if not sala:
        raise ValueError("Sala não encontrada.")

    return sala


def _exigir_dono_da_sala(usuario, sala):
    if not usuario:
        raise PermissionError("É necessário estar autenticado.")

    if usuario.get("tipo") not in {
        TIPO_PROPRIETARIO,
        TIPO_ADMIN,
    }:
        raise PermissionError(
            "Seu perfil não pode gerenciar salas."
        )

    login = _login_usuario(usuario)
    proprietario = (
        sala.get("proprietario") or ""
    ).strip().lower()

    # As salas de demonstração usam "ana" como proprietário padrão.
    dono_corresponde = (
        proprietario == login
        or (
            proprietario == "ana"
            and login.split("@", 1)[0] == "ana"
        )
    )

    if not dono_corresponde:
        raise PermissionError(
            "Você só pode gerenciar as salas associadas à sua conta."
        )


def atualizar_sala(
    usuario,
    sala_id,
    nome,
    capacidade,
    localizacao,
    recursos_marcados,
):
    sala = _buscar_sala(sala_id)
    _exigir_dono_da_sala(usuario, sala)

    dados_atualizados = sala_model.atualizar_sala(
        sala_id=sala_id,
        nome=nome,
        capacidade=capacidade,
        localizacao=localizacao,
        recursos_marcados=recursos_marcados,
    )

    recarregar_salas()
    return dados_atualizados


def excluir_sala(usuario, sala_id):
    sala = _buscar_sala(sala_id)
    _exigir_dono_da_sala(usuario, sala)

    status_que_impedem_exclusao = {
        reserva_model.PENDENTE,
        reserva_model.APROVADA,
    }

    reservas = reserva_model.listar_reservas()
    possui_reservas_ativas = any(
        str(reserva.get("sala_id")) == str(sala_id)
        and reserva.get("status") in status_que_impedem_exclusao
        for reserva in reservas
    )

    if possui_reservas_ativas:
        raise ValueError(
            "Não é possível excluir esta sala enquanto houver "
            "reservas pendentes ou aprovadas."
        )

    sala_model.excluir_sala(sala_id)
    recarregar_salas()