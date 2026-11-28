from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest


CONTA = {
    "uid": "locatario-teste",
    "nome": "Conta de Teste",
    "email": "teste@example.com",
    "perfil": "Locatário",
    "status": "ativo",
}


def preparar(monkeypatch, pagina="Início", secao=None, contas=None):
    from controllers import reserva_controller, usuario_firebase_controller
    from models import sala_firebase_model
    from views import admin_usuarios_firebase

    registros = [CONTA.copy()] if contas is None else contas
    listar = lambda usuario: registros
    monkeypatch.setattr(usuario_firebase_controller, "listar_usuarios_admin", listar)
    monkeypatch.setattr(admin_usuarios_firebase, "listar_usuarios_admin", listar)
    monkeypatch.setattr(reserva_controller, "listar_reservas_usuario", lambda usuario: [])
    monkeypatch.setattr(sala_firebase_model, "listar_salas", lambda: [])
    atualizar = Mock()
    monkeypatch.setattr(admin_usuarios_firebase, "atualizar_usuario_admin", atualizar)

    app = AppTest.from_string(f'''
import streamlit as st
from views.admin_view import mostrar_admin
if "usuario" not in st.session_state:
    st.session_state.usuario = {{
        "id": "admin-teste", "nome": "Administrador de Teste",
        "login": "admin", "tipo": "Administrador",
    }}
    st.session_state.admin_pagina = {pagina!r}
    st.session_state.admin_secao = {secao!r}
mostrar_admin()
''').run()
    assert not app.exception
    return app, atualizar


def clicar(app, chave):
    next(botao for botao in app.button if botao.key == chave).click().run()
    assert not app.exception


def conferir_lista_sem_cadastro(app):
    assert app.session_state["admin_pagina"] == "Usuários cadastrados"
    assert [item.value for item in app.subheader] == ["Contas cadastradas"]
    assert not any(campo.label in {"Usuário", "Senha inicial", "Nome completo *"}
                   for campo in app.text_input)
    assert not any(botao.label == "Criar usuário" for botao in app.button)


def test_menu_expoe_usuarios_acima_de_administracao(monkeypatch):
    app, _ = preparar(monkeypatch)
    chaves = [botao.key for botao in app.sidebar.button]
    assert chaves.index("side_Usuários cadastrados") < chaves.index("side_Administração")


@pytest.mark.parametrize("chave", ["side_Usuários cadastrados", "acao_Consultar usuários"])
def test_lista_abre_pelo_menu_e_pelo_atalho_sem_cadastro_simples(monkeypatch, chave):
    app, _ = preparar(monkeypatch)
    clicar(app, chave)
    conferir_lista_sem_cadastro(app)
    assert app.expander[0].label == "Conta de Teste — teste@example.com"


@pytest.mark.parametrize("chave", ["side_Administração", "acao_Cadastrar usuário", "admin_comecar"])
def test_cadastro_completo_continua_acessivel(monkeypatch, chave):
    app, _ = preparar(monkeypatch)
    clicar(app, chave)
    assert app.session_state["admin_pagina"] == "Administração"
    campos = {item.label for item in app.text_input}
    assert {"Nome completo *", "CPF *", "E-mail institucional *",
            "Telefone *", "Nome de usuário *", "Senha provisória *"} <= campos
    assert any(botao.label == "💾 Salvar cadastro" for botao in app.button)
    assert not any(botao.label == "Criar usuário" for botao in app.button)


def test_sessao_antiga_vai_para_lista_e_depois_abre_cadastro_correto(monkeypatch):
    app, _ = preparar(monkeypatch, pagina="Administração", secao="usuarios")
    conferir_lista_sem_cadastro(app)
    assert "admin_secao" not in app.session_state
    clicar(app, "side_Administração")
    assert any(campo.label == "CPF *" for campo in app.text_input)
    clicar(app, "side_Usuários cadastrados")
    conferir_lista_sem_cadastro(app)


def test_lista_vazia_nao_reintroduz_formulario_de_cadastro(monkeypatch):
    app, _ = preparar(monkeypatch, pagina="Usuários cadastrados", contas=[])
    conferir_lista_sem_cadastro(app)
    assert any("Ainda não há usuários" in item.value for item in app.info)
    assert not app.text_input


def test_edicao_de_conta_permanece_disponivel_na_lista(monkeypatch):
    app, atualizar = preparar(monkeypatch, pagina="Usuários cadastrados")
    next(campo for campo in app.text_input if campo.key == "nome_locatario-teste").set_value("Nome Atualizado")
    next(campo for campo in app.selectbox if campo.key == "status_locatario-teste").set_value("inativo")
    next(botao for botao in app.button if botao.label == "Salvar alterações").click().run()
    assert not app.exception
    atualizar.assert_called_once_with(
        app.session_state["usuario"], "locatario-teste", "Nome Atualizado",
        "teste@example.com", "Locatário", "inativo",
    )
    assert next(botao for botao in app.button if botao.label == "Excluir usuário").disabled
