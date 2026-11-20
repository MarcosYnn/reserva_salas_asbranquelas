from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Barrier

import pytest

from models import reserva_firebase_model as model
from models import sala_firebase_model as salas
from tests.firestore_fake import FirestoreFake


def pedido(inicio="09:00", fim="11:00", uid="u1", status="Pendente"):
    return dict(sala_id="s1", sala_nome="Sala", solicitante_uid=uid,
                solicitante_nome=uid, data="2030-05-11", hora_inicio=inicio,
                hora_fim=fim, status=status)


@pytest.fixture
def db(monkeypatch):
    banco = FirestoreFake({
        "salas/s1": {"id": "s1", "nome": "Nome atualizado", "proprietario": "dono"},
        "reservas/a": pedido(),
        "reservas/b": pedido("10:00", "12:00", "u2"),
    })
    monkeypatch.setattr(model, "obter_firestore", lambda: banco)
    monkeypatch.setattr(salas, "obter_firestore", lambda: banco)
    monkeypatch.setattr(model, "agora_local", lambda: datetime(2030, 5, 10, 12))
    return banco


def aprovar(id):
    model.alterar_status_reserva(id, model.APROVADA, "admin")


def test_rejeita_segunda_aprovacao_sobreposta(db):
    aprovar("a")
    with pytest.raises(ValueError, match="ocupa este horário"):
        aprovar("b")
    assert db.data["reservas/b"]["status"] == model.PENDENTE


def test_aprovacao_e_independente_em_outro_dia(db):
    db.data["reservas/b"]["data"] = "2030-05-12"
    aprovar("a")
    aprovar("b")
    assert db.data["reservas/b"]["status"] == model.APROVADA


def test_aprovacao_e_independente_em_outra_sala(db):
    db.data["salas/s2"] = {"id": "s2", "nome": "Outra sala"}
    db.data["reservas/b"]["sala_id"] = "s2"
    aprovar("a")
    aprovar("b")
    assert db.data["reservas/b"]["status"] == model.APROVADA


@pytest.mark.parametrize("data,inicio,fim", [
    ("2030-5-11", "09:00", "11:00"),
    ("2030-05-11", "9:00", "11:00"),
    ("2030-05-11", "09:00", "11:0"),
])
def test_periodos_sao_canonicos_para_nao_burlar_conflito(db, data, inicio, fim):
    with pytest.raises(ValueError):
        model._validar_data_horarios(data, inicio, fim)


def test_disputa_simultanea_produz_uma_unica_aprovacao(db):
    db.barrier = Barrier(2)
    def tentar(id):
        try:
            aprovar(id)
            return "aprovada"
        except ValueError:
            return "conflito"
    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(tentar, ("a", "b")))
    assert sorted(resultados) == ["aprovada", "conflito"]
    assert db.aborts == 1
    assert sum(d["status"] == model.APROVADA for p, d in db.data.items()
               if p.startswith("reservas/")) == 1


def test_intervalos_adjacentes_sao_aprovados(db):
    db.data["reservas/b"].update(hora_inicio="11:00", hora_fim="12:00")
    aprovar("a")
    aprovar("b")
    assert db.data["reservas/b"]["status"] == model.APROVADA


def test_cancelamento_libera_horario(db):
    aprovar("a")
    model.alterar_status_reserva("a", model.CANCELADA, "u1", solicitante_uid="u1")
    aprovar("b")
    assert db.data["reservas/b"]["status"] == model.APROVADA


def test_titularidade_conferida_na_transacao(db):
    with pytest.raises(PermissionError):
        model.alterar_status_reserva("a", model.CANCELADA, "u2", solicitante_uid="u2")
    assert db.data["reservas/a"]["status"] == model.PENDENTE


def test_aprovacao_de_sala_removida_e_recusada(db):
    del db.data["salas/s1"]
    with pytest.raises(ValueError, match="não está mais disponível"):
        aprovar("a")


def test_aprovacao_de_pedido_que_ja_passou_e_recusada(db, monkeypatch):
    monkeypatch.setattr(model, "agora_local", lambda: datetime(2030, 5, 11, 10))
    with pytest.raises(ValueError, match="posterior ao horário atual"):
        aprovar("a")


def criar(uid="u3"):
    return model.criar_reserva("s1", "Nome antigo", "login_antigo", uid, uid,
                              "2030-05-11", "09:00", "11:00")


def test_criacao_recarrega_sala_e_sinaliza_conflito(db):
    id = criar()
    assert db.data["reservas/" + id]["sala_nome"] == "Nome atualizado"
    assert db.data["reservas/" + id]["precisa_revisao_admin"] is True
    assert set(db.data["reservas/" + id]["conflitos_reserva_ids"]) == {"a", "b"}


def test_duplo_clique_nao_duplica_pedido(db):
    criar()
    with pytest.raises(ValueError, match="já tem um pedido ativo"):
        criar()


def test_criacao_simultanea_nao_duplica_pedido(db):
    db.barrier = Barrier(2)
    def tentar(_):
        try:
            criar()
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=2) as executor:
        assert sum(executor.map(tentar, (1, 2))) == 1
    assert db.aborts == 1


def test_novo_pedido_e_permitido_apos_cancelamento(db):
    id = criar()
    model.alterar_status_reserva(id, model.CANCELADA, "u3", solicitante_uid="u3")
    assert criar() != id


def test_pedidos_pendentes_de_usuarios_distintos_podem_coexistir(db):
    assert criar("u3") != criar("u4")


def test_criacao_em_sala_removida_nao_grava_pedido(db):
    del db.data["salas/s1"]
    with pytest.raises(ValueError, match="não está mais disponível"):
        criar()
    assert len(db.data) == 2


def test_registro_aprovado_malformado_nao_libera_aprovacao(db):
    db.data["reservas/a"].update(status=model.APROVADA, hora_inicio="inválido")
    with pytest.raises(ValueError, match="horário inválido"):
        aprovar("b")


def test_exclusao_com_pedido_ativo_e_bloqueada(db):
    with pytest.raises(ValueError, match="pedidos pendentes ou aprovados"):
        salas.excluir_sala("s1")
    assert "salas/s1" in db.data


def test_criacao_e_exclusao_simultaneas_nao_deixam_pedido_orfao(db):
    db.data.pop("reservas/a")
    db.data.pop("reservas/b")
    db.barrier = Barrier(2)
    def tentar(acao):
        try:
            acao()
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(tentar, (criar, lambda: salas.excluir_sala("s1"))))
    assert sum(resultados) == 1
    if any(p.startswith("reservas/") for p in db.data):
        assert "salas/s1" in db.data
    assert db.aborts == 1
