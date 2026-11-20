from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import streamlit as st

from controllers import sessao_controller as sessao
from controllers import firebase_auth_controller as login
from controllers import usuario_firebase_controller as usuarios
from controllers import favorito_controller as favoritos
from controllers import sala_controller as salas
from models import favorito_firebase_model as favorito_model
from utils.sessao import limpar_dados_usuario
from utils.busca import invalidar_busca_se_alterada
from tests.firestore_fake import FirestoreFake


class Estado(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value


@pytest.fixture
def acesso(monkeypatch):
    estado = Estado(inicializado_firebase=True, salas=[], favoritos={"s1"},
                    busca_data_iso="2030-01-01", admin_pagina="Reservas",
                    resultado_busca=[{"id": "s1"}], rota_campus={"destino": "Sala"})
    monkeypatch.setattr(st, "session_state", estado)
    perfil = dict(uid="u1", usuario="arthur", nome="Arthur", email="a@example.com",
                  perfil="Administrador", status="ativo")
    conta = SimpleNamespace(uid="u1", email="a@example.com", disabled=False)
    monkeypatch.setattr(sessao.usuario_model, "buscar_usuario", lambda uid: perfil)
    monkeypatch.setattr(sessao, "obter_app_firebase", lambda: None)
    monkeypatch.setattr(sessao.auth, "get_user", lambda *args, **kwargs: conta)
    usuario = dict(id="u1", login="arthur", tipo="Administrador", nome="Arthur")
    estado.usuario = usuario
    return usuario, perfil, conta, estado


def test_bloqueio_afeta_sessao_aberta(acesso):
    usuario, perfil, _, estado = acesso
    perfil["status"] = "inativo"
    with pytest.raises(PermissionError):
        sessao.revalidar_usuario(usuario)
    assert estado.usuario is None
    assert estado.favoritos == set()
    assert "busca_data_iso" not in estado


def test_bloqueio_no_auth_afeta_sessao_aberta(acesso):
    usuario, _, conta, _ = acesso
    conta.disabled = True
    with pytest.raises(PermissionError):
        sessao.revalidar_usuario(usuario)


def test_mudanca_de_perfil_atualiza_usuario_e_limpa_navegacao(acesso):
    usuario, perfil, _, estado = acesso
    perfil["perfil"] = "Locatário"
    sessao.revalidar_usuario(usuario)
    assert usuario["tipo"] == "Locatário"
    assert estado.usuario is usuario
    assert "admin_pagina" not in estado
    assert "rota_campus" not in estado


def test_admin_rebaixado_nao_executa_acao_administrativa(acesso, monkeypatch):
    usuario, perfil, _, _ = acesso
    perfil["perfil"] = "Locatário"
    listar = Mock()
    monkeypatch.setattr(usuarios.model, "listar_usuarios", listar)
    with pytest.raises(PermissionError):
        usuarios.listar_usuarios_admin(usuario)
    listar.assert_not_called()


def test_uid_de_perfil_divergente_e_rejeitado(acesso):
    usuario, perfil, _, _ = acesso
    perfil["uid"] = "outra_conta"
    with pytest.raises(PermissionError):
        sessao.revalidar_usuario(usuario)


def test_falha_de_consulta_nao_autoriza_por_cache(acesso, monkeypatch):
    usuario, _, _, _ = acesso
    monkeypatch.setattr(sessao.usuario_model, "buscar_usuario",
                        Mock(side_effect=RuntimeError("offline")))
    with pytest.raises(PermissionError, match="verificar seu acesso"):
        usuarios.listar_usuarios_admin(usuario)


def test_conta_excluida_perde_acesso(acesso, monkeypatch):
    usuario, _, _, estado = acesso
    monkeypatch.setattr(sessao.usuario_model, "buscar_usuario", lambda uid: None)
    with pytest.raises(PermissionError):
        sessao.revalidar_usuario(usuario)
    assert estado.usuario is None


def test_logout_limpa_dados_e_preserva_inicializacao(acesso):
    _, _, _, estado = acesso
    limpar_dados_usuario()
    assert estado == dict(inicializado_firebase=True, salas=[], usuario=None,
                          favoritos=set(), resultado_busca=None)


def test_login_rejeita_uid_auth_diferente_do_documento(acesso, monkeypatch):
    _, perfil, _, estado = acesso
    perfil["uid"] = "uid_incorreto"
    monkeypatch.setattr(login.usuario_model, "buscar_usuario_por_usuario", lambda usuario: perfil)
    monkeypatch.setattr(st, "secrets", {"firebase": {"web_api_key": "teste"}})
    monkeypatch.setattr(login.requests, "post", lambda *a, **k: SimpleNamespace(
        status_code=200, json=lambda: {"localId": "u1", "idToken": "token_teste"}))
    monkeypatch.setattr(login, "obter_app_firebase", lambda: None)
    monkeypatch.setattr(login.firebase_auth, "verify_id_token", lambda *a, **k: {"uid": "u1"})
    assert login.autenticar_usuario_firebase("arthur", "senha")[0] is False


def test_login_bem_sucedido_descarta_dados_anteriores(acesso, monkeypatch):
    _, perfil, _, estado = acesso
    monkeypatch.setattr(login.usuario_model, "buscar_usuario_por_usuario", lambda usuario: perfil)
    monkeypatch.setattr(st, "secrets", {"firebase": {"web_api_key": "teste"}})
    monkeypatch.setattr(login.requests, "post", lambda *a, **k: SimpleNamespace(
        status_code=200, json=lambda: {"localId": "u1", "idToken": "token_teste"}))
    monkeypatch.setattr(login, "obter_app_firebase", lambda: None)
    monkeypatch.setattr(login.firebase_auth, "verify_id_token", lambda *a, **k: {"uid": "u1"})
    assert login.autenticar_usuario_firebase("arthur", "senha")[0] is True
    assert estado.usuario["id"] == "u1"
    assert estado.favoritos == set()
    assert "busca_data_iso" not in estado


def test_favoritos_persistem_por_uid_e_ficam_isolados(acesso, monkeypatch):
    usuario, perfil, _, _ = acesso
    perfil["perfil"] = "Locatário"
    db = FirestoreFake({"salas/s1": {"nome": "Sala"}})
    monkeypatch.setattr(favorito_model, "obter_firestore", lambda: db)
    favoritos.definir_favorito(usuario, "s1", True)
    assert favoritos.listar_favoritos(usuario) == {"s1"}
    assert favorito_model.listar_favoritos("u2") == set()
    limpar_dados_usuario()
    assert favoritos.listar_favoritos(usuario) == {"s1"}
    favoritos.definir_favorito(usuario, "s1", False)
    assert favoritos.listar_favoritos(usuario) == set()


def test_favoritar_sala_removida_e_recusado(acesso, monkeypatch):
    usuario, perfil, _, _ = acesso
    perfil["perfil"] = "Locatário"
    monkeypatch.setattr(favorito_model, "obter_firestore", lambda: FirestoreFake())
    with pytest.raises(ValueError, match="não está mais disponível"):
        favoritos.definir_favorito(usuario, "s1", True)


def test_alterar_filtros_descarta_periodo_e_resultados():
    estado = dict(criterios_busca=("antigo",), busca_data_iso="2030-01-01",
                  busca_hora_inicio="09:00", busca_hora_fim="10:00",
                  busca_conflitos_por_sala={"s1": []}, resultado_busca=[{"id": "s1"}])
    invalidar_busca_se_alterada(estado, ("novo",))
    assert estado == dict(criterios_busca=("novo",), resultado_busca=None)


def test_filtros_iguais_preservam_resultados():
    estado = dict(criterios_busca=("igual",), resultado_busca=[{"id": "s1"}])
    invalidar_busca_se_alterada(estado, ("igual",))
    assert estado["resultado_busca"] == [{"id": "s1"}]


def test_admin_pode_gerenciar_sala_de_outro_proprietario(acesso):
    usuario, _, _, _ = acesso
    salas._exigir_dono_da_sala(usuario, {"proprietario": "outro"})


def test_proprietario_nao_gerencia_sala_alheia(acesso):
    usuario, perfil, _, _ = acesso
    perfil["perfil"] = "Proprietário"
    with pytest.raises(PermissionError):
        salas._exigir_dono_da_sala(usuario, {"proprietario": "outro"})
