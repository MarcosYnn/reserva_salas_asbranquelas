from datetime import timedelta, time
from unittest.mock import Mock

from streamlit.testing.v1 import AppTest

from utils.relogio import hoje_local


SALAS = [
    {"id": "s1", "nome": "Laboratório", "capacidade": 12, "andar": "2º andar",
     "recursos": "Projetor", "projetor": True},
    {"id": "s2", "nome": "Sala simples", "capacidade": 8, "andar": "1º andar",
     "recursos": "Quadro", "quadro": True},
]


def preparar(monkeypatch, pagina):
    import main
    from controllers import sessao_controller
    monkeypatch.setattr(sessao_controller, "revalidar_usuario", lambda usuario: usuario)
    monkeypatch.setattr(main, "listar_reservas_ativas_para_busca", lambda usuario: [])
    app = AppTest.from_string(f"""
import streamlit as st
from main import {pagina}
if "usuario" not in st.session_state:
    st.session_state.usuario = {{"id": "u1", "nome": "Arthur", "tipo": "Locatário"}}
    st.session_state.salas = {SALAS!r}
    st.session_state.favoritos = {{"s1"}}
    st.session_state.resultado_busca = None
{pagina}(st.session_state.usuario)
""").run()
    assert not app.exception
    return app


def test_busca_invalida_resultados_ao_alterar_periodo(monkeypatch):
    app = preparar(monkeypatch, "pagina_buscar_salas")
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    app.button[0].click().run()
    assert not app.exception
    assert len([b for b in app.button if b.label == "Confirmar pedido"]) == 2
    app.time_input[0].set_value(time(11)).run()
    assert not app.exception
    assert not [b for b in app.button if b.label == "Confirmar pedido"]


def test_filtros_de_localizacao_e_recurso_alteram_resultados(monkeypatch):
    app = preparar(monkeypatch, "pagina_buscar_salas")
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    app.text_input[0].set_value("2º")
    app.multiselect[0].set_value(["projetor"])
    app.button[0].click().run()
    assert not app.exception
    assert len([b for b in app.button if b.label == "Confirmar pedido"]) == 1
    assert "1 sala(s)" in app.success[0].value


def test_favoritos_solicita_periodo_sem_busca_anterior(monkeypatch):
    from utils import componentes
    enviar = Mock()
    monkeypatch.setattr(componentes, "criar_pedido_reserva", enviar)
    app = preparar(monkeypatch, "pagina_favoritos")
    amanha = hoje_local() + timedelta(days=1)
    app.date_input[0].set_value(amanha)
    app.time_input[0].set_value(time(14))
    app.time_input[1].set_value(time(15))
    next(b for b in app.button if b.label == "Confirmar pedido").click().run()
    assert not app.exception
    assert enviar.call_count == 1
    assert enviar.call_args.kwargs["data"] == amanha.isoformat()
    assert enviar.call_args.kwargs["hora_inicio"] == "14:00"
    assert enviar.call_args.kwargs["hora_fim"] == "15:00"


def test_erro_de_disponibilidade_nao_exibe_salas_como_validadas(monkeypatch):
    app = preparar(monkeypatch, "pagina_buscar_salas")
    import main
    monkeypatch.setattr(main, "listar_reservas_ativas_para_busca",
                        Mock(side_effect=RuntimeError("indisponível")))
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    app.button[0].click().run()
    assert not app.exception
    assert app.error
    assert not [b for b in app.button if b.label == "Confirmar pedido"]
