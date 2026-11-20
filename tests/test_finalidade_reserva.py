"""Regressão do card PraxiLab 1844e81e-de39-4390-b2ec-d2b88f897013."""

from datetime import datetime
from unittest.mock import Mock

import pytest

from controllers import reserva_controller as controller
from controllers import sessao_controller
from models import reserva_firebase_model as model
from tests.firestore_fake import FirestoreFake


@pytest.fixture
def ambiente(monkeypatch):
    banco = FirestoreFake({
        "salas/s1": {"id": "s1", "nome": "Laboratório", "proprietario": "dono"},
    })
    monkeypatch.setattr(model, "obter_firestore", lambda: banco)
    monkeypatch.setattr(model, "agora_local", lambda: datetime(2030, 5, 10, 12))
    monkeypatch.setattr(sessao_controller, "revalidar_usuario", lambda usuario: usuario)
    return banco


def criar_modelo(**opcoes):
    return model.criar_reserva(
        "s1", "Laboratório", "dono", "u1", "Arthur",
        "2030-05-11", "09:00", "10:00", **opcoes,
    )


def criar_controller(finalidade=""):
    return controller.criar_pedido_reserva(
        {"id": "u1", "nome": "Arthur", "tipo": "Locatário"},
        {"id": "s1", "nome": "Laboratório", "proprietario": "dono"},
        "2030-05-11", "09:00", "10:00", finalidade=finalidade,
    )


def test_persiste_finalidade_normalizada_e_retorna_na_consulta(ambiente):
    id = criar_modelo(finalidade="  Reunião da equipe de TCC.\n  ")
    assert ambiente.data["reservas/" + id]["finalidade"] == "Reunião da equipe de TCC."
    assert model.buscar_reserva(id)["finalidade"] == "Reunião da equipe de TCC."
    assert model.listar_reservas()[0]["finalidade"] == "Reunião da equipe de TCC."


@pytest.mark.parametrize("finalidade", ["", " \n\t ", None])
def test_finalidade_vazia_e_opcional(ambiente, finalidade):
    id = criar_modelo(finalidade=finalidade)
    assert ambiente.data["reservas/" + id]["finalidade"] == ""


def test_assinatura_antiga_sem_finalidade_continua_funcionando(ambiente):
    id = criar_modelo()
    assert ambiente.data["reservas/" + id]["finalidade"] == ""


def test_aceita_limite_500_depois_de_remover_espacos(ambiente):
    finalidade = "á" * 500
    id = criar_modelo(finalidade="  " + finalidade + "  ")
    assert ambiente.data["reservas/" + id]["finalidade"] == finalidade


@pytest.mark.parametrize("finalidade", ["a" * 501, 0, 42, True, [], {}, b"reuniao"])
def test_rejeita_excesso_ou_tipo_invalido_sem_gravar(ambiente, finalidade):
    with pytest.raises(ValueError, match="finalidade"):
        criar_modelo(finalidade=finalidade)
    assert list(ambiente.data) == ["salas/s1"]
    assert "reservas_atualizadas_em" not in ambiente.data["salas/s1"]


def test_controller_encaminha_finalidade_normalizada(ambiente):
    id = criar_controller("  Aula prática de redes  ")
    assert model.buscar_reserva(id)["finalidade"] == "Aula prática de redes"


def test_controller_rejeita_finalidade_antes_de_listar_ou_gravar(ambiente, monkeypatch):
    listar = Mock()
    gravar = Mock()
    monkeypatch.setattr(model, "listar_reservas", listar)
    monkeypatch.setattr(model, "criar_reserva", gravar)
    with pytest.raises(ValueError, match="500"):
        criar_controller("a" * 501)
    listar.assert_not_called()
    gravar.assert_not_called()


def test_alterar_status_preserva_finalidade(ambiente):
    id = criar_modelo(finalidade="Defesa do trabalho")
    model.alterar_status_reserva(id, model.APROVADA, "admin")
    model.alterar_status_reserva(id, model.CANCELADA, "u1", solicitante_uid="u1")
    assert model.buscar_reserva(id)["finalidade"] == "Defesa do trabalho"


def test_finalidade_nao_permite_burlar_pedido_duplicado(ambiente):
    criar_modelo(finalidade="Reunião")
    with pytest.raises(ValueError, match="pedido ativo"):
        criar_modelo(finalidade="Outra finalidade")


def test_registro_antigo_sem_campo_continua_consultavel(ambiente):
    id = criar_modelo()
    del ambiente.data["reservas/" + id]["finalidade"]
    assert model.buscar_reserva(id)["id"] == id
    assert "finalidade" not in model.buscar_reserva(id)
