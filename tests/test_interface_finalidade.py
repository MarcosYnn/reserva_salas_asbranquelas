from datetime import time, timedelta
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from tests.test_interface_reservas import preparar
from utils.relogio import hoje_local


@pytest.mark.parametrize("pagina", ["pagina_buscar_salas", "pagina_favoritos"])
def test_formularios_encaminham_finalidade_sem_mudar_periodo(monkeypatch, pagina):
    from utils import componentes
    criar = Mock()
    monkeypatch.setattr(componentes, "criar_pedido_reserva", criar)
    app = preparar(monkeypatch, pagina)
    amanha = hoje_local() + timedelta(days=1)
    app.date_input[0].set_value(amanha)
    app.time_input[0].set_value(time(14))
    app.time_input[1].set_value(time(15))
    app.text_area[0].set_value("Aula prática de redes")
    if pagina == "pagina_buscar_salas":
        next(b for b in app.button if b.label == "🔎 Procurar salas").click().run()
    next(b for b in app.button if b.label == "Confirmar pedido").click().run()
    assert not app.exception
    assert criar.call_count == 1
    assert criar.call_args.kwargs["finalidade"] == "Aula prática de redes"
    assert criar.call_args.kwargs["data"] == amanha.isoformat()
    assert criar.call_args.kwargs["hora_inicio"] == "14:00"
    assert criar.call_args.kwargs["hora_fim"] == "15:00"


def test_editar_finalidade_apos_busca_envia_texto_atual(monkeypatch):
    from utils import componentes
    criar = Mock()
    monkeypatch.setattr(componentes, "criar_pedido_reserva", criar)
    app = preparar(monkeypatch, "pagina_buscar_salas")
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    app.text_area[0].set_value("Finalidade anterior")
    next(b for b in app.button if b.label == "🔎 Procurar salas").click().run()
    app.text_area[0].set_value("Finalidade atualizada").run()
    next(b for b in app.button if b.label == "Confirmar pedido").click().run()
    assert not app.exception
    assert criar.call_args.kwargs["finalidade"] == "Finalidade atualizada"


@pytest.mark.parametrize("pagina", ["pagina_buscar_salas", "pagina_favoritos"])
def test_formularios_continuam_permitindo_finalidade_vazia(monkeypatch, pagina):
    from utils import componentes
    criar = Mock()
    monkeypatch.setattr(componentes, "criar_pedido_reserva", criar)
    app = preparar(monkeypatch, pagina)
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    if pagina == "pagina_buscar_salas":
        next(b for b in app.button if b.label == "🔎 Procurar salas").click().run()
    next(b for b in app.button if b.label == "Confirmar pedido").click().run()
    assert not app.exception
    assert criar.call_args.kwargs["finalidade"] == ""


@pytest.mark.parametrize("perfil", ["Locatário", "Proprietário", "Administrador"])
@pytest.mark.parametrize("finalidade", ["Reunião de planejamento", None])
def test_detalhes_dos_tres_perfis_mostram_finalidade_ou_fallback(monkeypatch, perfil, finalidade):
    from controllers import sessao_controller
    from views import reserva_view
    monkeypatch.setattr(sessao_controller, "revalidar_usuario", lambda usuario: usuario)
    registro = dict(id="r1", sala_nome="Sala", solicitante_nome="Arthur",
                    data="2030-05-11", hora_inicio="09:00", hora_fim="10:00",
                    status="Aprovada")
    if finalidade is not None:
        registro["finalidade"] = finalidade
    # A autorização continua a cargo do controller; aqui se verifica a apresentação.
    monkeypatch.setattr(reserva_view, "listar_reservas_usuario", lambda usuario: [registro])
    app = AppTest.from_string(f"""
from views.reserva_view import renderizar_reservas
renderizar_reservas({{"id":"u1", "tipo":{perfil!r}}})
""").run()
    assert not app.exception
    assert (finalidade or "Não informada") in [elemento.value for elemento in app.text]


def test_finalidade_e_exibida_como_texto_sem_interpretar_markdown():
    texto = "**Reunião** <script>alert(1)</script> ![imagem](https://exemplo.invalid/img)"
    app = AppTest.from_string(f"""
from views.reserva_view import _mostrar_reserva
_mostrar_reserva({{"finalidade":{texto!r}}})
""").run()
    assert not app.exception
    assert texto in [elemento.value for elemento in app.text]
    assert not app.get("imgs")


@pytest.mark.parametrize("pagina", ["pagina_buscar_salas", "pagina_favoritos"])
def test_erro_de_validacao_do_servidor_aparece_na_interface(monkeypatch, pagina):
    from utils import componentes
    criar = Mock(side_effect=ValueError("A finalidade da reserva deve ter no máximo 500 caracteres."))
    monkeypatch.setattr(componentes, "criar_pedido_reserva", criar)
    app = preparar(monkeypatch, pagina)
    app.date_input[0].set_value(hoje_local() + timedelta(days=1))
    if pagina == "pagina_buscar_salas":
        next(b for b in app.button if b.label == "🔎 Procurar salas").click().run()
    next(b for b in app.button if b.label == "Confirmar pedido").click().run()
    assert not app.exception
    assert "500 caracteres" in app.error[0].value
