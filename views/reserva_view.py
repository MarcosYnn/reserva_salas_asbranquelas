from datetime import datetime

import streamlit as st

from controllers.reserva_controller import (
    alterar_status_reserva_admin,
    cancelar_reserva_locatario,
    listar_reservas_usuario,
)
from models import reserva_firebase_model as reserva_model
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
)


ROTULOS_PRIORIDADE = {
    1: "Normal",
    2: "Aula prática / precisa de equipamentos",
    3: "Evento institucional",
}


def _formatar_data(data):
    try:
        return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return data or "Data não informada"


def _mostrar_reserva(reserva, mostrar_revisao_admin=False):
    st.write(f"**Sala:** {reserva.get('sala_nome', 'Sala sem nome')}")
    st.write(f"**Solicitante:** {reserva.get('solicitante_nome', '—')}")
    st.write(f"**Data:** {_formatar_data(reserva.get('data'))}")
    st.write(
        f"**Horário:** {reserva.get('hora_inicio', '—')} "
        f"às {reserva.get('hora_fim', '—')}"
    )
    st.write(f"**Status:** {reserva.get('status', '—')}")

    if not mostrar_revisao_admin:
        return

    prioridade = reserva.get("prioridade", 1)
    rotulo_prioridade = ROTULOS_PRIORIDADE.get(
        prioridade,
        "Não definida",
    )
    st.write(f"**Prioridade:** {rotulo_prioridade}")

    if not reserva.get("precisa_revisao_admin"):
        return

    st.warning(
        "Este pedido coincide com outra reserva pendente ou aprovada. "
        "Confira os detalhes antes de decidir."
    )

    conflitos_ids = reserva.get("conflitos_reserva_ids", [])
    if not conflitos_ids:
        st.caption(
            "O pedido foi sinalizado para revisão, mas não há "
            "identificadores de conflito registrados."
        )
        return

    st.markdown("**Reservas que geraram o alerta:**")

    for conflito_id in conflitos_ids:
        try:
            conflito = reserva_model.buscar_reserva(conflito_id)
        except Exception as erro:
            st.caption(
                f"Não foi possível consultar o pedido {conflito_id}: {erro}"
            )
            continue

        if not conflito:
            st.caption(f"Pedido relacionado não encontrado: {conflito_id}")
            continue

        st.write(
            f"- **{conflito.get('sala_nome', 'Sala')}** — "
            f"{_formatar_data(conflito.get('data'))}, "
            f"{conflito.get('hora_inicio', '—')} às "
            f"{conflito.get('hora_fim', '—')} — "
            f"{conflito.get('status', 'Status não informado')} "
            f"(solicitante: {conflito.get('solicitante_nome', '—')})"
        )


def _alterar_status_e_atualizar(usuario, reserva_id, novo_status):
    try:
        alterar_status_reserva_admin(
            usuario,
            reserva_id,
            novo_status,
        )
        st.success(f"Reserva marcada como {novo_status.lower()}.")
        st.rerun()
    except Exception as erro:
        st.error(str(erro))


def _cancelar_e_atualizar(usuario, reserva_id):
    try:
        cancelar_reserva_locatario(usuario, reserva_id)
        st.success("Pedido cancelado.")
        st.rerun()
    except Exception as erro:
        st.error(str(erro))


def renderizar_reservas(usuario):
    perfil = usuario.get("tipo")

    if perfil not in {
        TIPO_ADMIN,
        TIPO_LOCATARIO,
        TIPO_PROPRIETARIO,
    }:
        st.error("Seu perfil não pode consultar reservas.")
        return

    if perfil == TIPO_ADMIN:
        st.subheader("Pedidos de reserva")
    elif perfil == TIPO_PROPRIETARIO:
        st.subheader("Pedidos para as suas salas")
    else:
        st.subheader("Minhas reservas")

    try:
        reservas = listar_reservas_usuario(usuario)
    except Exception as erro:
        st.error(f"Não foi possível carregar as reservas: {erro}")
        return

    if not reservas:
        st.info("Nenhum pedido de reserva encontrado.")
        return

    for reserva in reservas:
        reserva_id = reserva["id"]
        status = reserva.get("status", "Pendente")

        with st.expander(
            f"{reserva.get('sala_nome', 'Sala')} — "
            f"{_formatar_data(reserva.get('data'))} — {status}"
        ):
            _mostrar_reserva(
                reserva,
                mostrar_revisao_admin=(perfil == TIPO_ADMIN),
            )

            if perfil == TIPO_ADMIN:
                if status == reserva_model.PENDENTE:
                    col_aprovar, col_recusar, col_cancelar = st.columns(3)

                    with col_aprovar:
                        if st.button(
                            "Aprovar",
                            key=f"aprovar_{reserva_id}",
                            type="primary",
                        ):
                            _alterar_status_e_atualizar(
                                usuario,
                                reserva_id,
                                reserva_model.APROVADA,
                            )

                    with col_recusar:
                        if st.button(
                            "Recusar",
                            key=f"recusar_{reserva_id}",
                        ):
                            _alterar_status_e_atualizar(
                                usuario,
                                reserva_id,
                                reserva_model.RECUSADA,
                            )

                    with col_cancelar:
                        if st.button(
                            "Cancelar",
                            key=f"cancelar_admin_{reserva_id}",
                        ):
                            _alterar_status_e_atualizar(
                                usuario,
                                reserva_id,
                                reserva_model.CANCELADA,
                            )

                elif status == reserva_model.APROVADA:
                    if st.button(
                        "Cancelar reserva",
                        key=f"cancelar_admin_{reserva_id}",
                    ):
                        _alterar_status_e_atualizar(
                            usuario,
                            reserva_id,
                            reserva_model.CANCELADA,
                        )

            elif (
                perfil == TIPO_LOCATARIO
                and status in {
                    reserva_model.PENDENTE,
                    reserva_model.APROVADA,
                }
            ):
                if st.button(
                    "Cancelar meu pedido",
                    key=f"cancelar_locatario_{reserva_id}",
                ):
                    _cancelar_e_atualizar(usuario, reserva_id)