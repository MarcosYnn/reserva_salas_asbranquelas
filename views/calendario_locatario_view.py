from utils.relogio import hoje_local
import calendar
from datetime import date

import streamlit as st

from controllers.autorizacao_controller import exigir_tipo
from controllers.reserva_controller import listar_reservas_usuario
from models import reserva_firebase_model as reserva_model
from utils.estado import MAPA_RECURSOS, TIPO_LOCATARIO, sala_por_id


MESES = (
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
)

DIAS_SEMANA = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")


def renderizar_calendario_locatario(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="page-intro">'
        "Visualize suas reservas organizadas por dia e acompanhe o status de cada pedido."
        "</div>",
        unsafe_allow_html=True,
    )

    chave_mes = "calendario_locatario_mes"
    if chave_mes not in st.session_state:
        hoje = hoje_local()
        st.session_state[chave_mes] = date(hoje.year, hoje.month, 1)

    mes_atual = st.session_state[chave_mes]
    col_anterior, col_titulo, col_proximo = st.columns([1, 5, 1])

    with col_anterior:
        if st.button("‹ Anterior", key="calendario_locatario_anterior"):
            ano = mes_atual.year
            mes = mes_atual.month - 1
            if mes == 0:
                ano -= 1
                mes = 12
            st.session_state[chave_mes] = date(ano, mes, 1)
            st.rerun()

    with col_titulo:
        st.markdown(
            f"<h3 style='text-align:center; margin:0.35rem 0;'>"
            f"{MESES[mes_atual.month - 1].capitalize()} de {mes_atual.year}"
            "</h3>",
            unsafe_allow_html=True,
        )

    with col_proximo:
        if st.button("Próximo ›", key="calendario_locatario_proximo"):
            ano = mes_atual.year
            mes = mes_atual.month + 1
            if mes == 13:
                ano += 1
                mes = 1
            st.session_state[chave_mes] = date(ano, mes, 1)
            st.rerun()

    try:
        reservas = listar_reservas_usuario(usuario)
    except Exception as erro:
        st.error(f"Não foi possível carregar suas reservas: {erro}")
        return

    # Neste calendário, somente pedidos confirmados aparecem como eventos.
    reservas_confirmadas = [
        reserva
        for reserva in reservas
        if reserva.get("status") == reserva_model.APROVADA
    ]

    reservas_por_data = {}
    for reserva in reservas_confirmadas:
        data_reserva = reserva.get("data")
        if data_reserva:
            reservas_por_data.setdefault(data_reserva, []).append(reserva)

    for lista in reservas_por_data.values():
        lista.sort(key=lambda item: item.get("hora_inicio", ""))

    st.caption("O calendário mostra apenas reservas aprovadas/confirmadas.")
    st.markdown("🟢 Reserva confirmada")

    cabecalho = st.columns(7)
    for coluna, nome_dia in zip(cabecalho, DIAS_SEMANA):
        coluna.markdown(f"**{nome_dia}**")

    calendario_mes = calendar.Calendar(firstweekday=0)
    semanas = calendario_mes.monthdayscalendar(mes_atual.year, mes_atual.month)

    for semana in semanas:
        colunas = st.columns(7)
        for coluna, numero_dia in zip(colunas, semana):
            with coluna:
                if numero_dia == 0:
                    st.markdown("&nbsp;", unsafe_allow_html=True)
                    continue

                data_iso = date(
                    mes_atual.year,
                    mes_atual.month,
                    numero_dia,
                ).isoformat()

                with st.container(border=True):
                    st.markdown(f"**{numero_dia}**")

                    eventos = reservas_por_data.get(data_iso, [])
                    if not eventos:
                        st.caption("—")
                        continue

                    for reserva in eventos:
                        horario = (
                            f"{reserva.get('hora_inicio', '—')}–"
                            f"{reserva.get('hora_fim', '—')}"
                        )
                        sala = reserva.get("sala_nome", "Sala")
                        st.caption(f"🟢 {horario}")

                        with st.expander(
                            f"🏢 {sala} · Ver detalhes",
                            expanded=False,
                        ):
                            st.write(f"**Horário:** {horario}")
                            st.write("**Status:** Confirmada")

                            try:
                                detalhes_sala = sala_por_id(
                                    reserva.get("sala_id")
                                )
                            except (ValueError, TypeError):
                                detalhes_sala = None

                            if detalhes_sala:
                                st.write(
                                    "**Capacidade:** "
                                    f"{detalhes_sala.get('capacidade', '—')} pessoas"
                                )
                                st.write(
                                    "**Localização:** "
                                    f"{detalhes_sala.get('andar') or detalhes_sala.get('localizacao') or 'Não informada'}"
                                )
                                recursos = [
                                    rotulo
                                    for chave, rotulo in MAPA_RECURSOS
                                    if detalhes_sala.get(chave)
                                ]
                                st.write(
                                    "**Recursos:** "
                                    + (", ".join(recursos) if recursos else "Nenhum informado")
                                )
                            else:
                                st.caption(
                                    "Os detalhes completos desta sala não estão disponíveis."
                                )

    if not reservas_confirmadas:
        st.info("Você ainda não tem reservas confirmadas neste calendário.")

