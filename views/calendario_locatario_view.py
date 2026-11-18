
import calendar
from datetime import date, datetime

import streamlit as st

from controllers.autorizacao_controller import exigir_tipo
from utils.estado import (
    reservas_de,
    MAPA_RECURSOS,
    TIPO_LOCATARIO,
    sala_por_id,
)


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

    # ==========================================
    # CABEÇALHO
    # ==========================================

    st.title("📅 Calendário de Reservas")

    st.markdown(
        "Visualize suas reservas organizadas por dia "
        "e acompanhe o status de cada pedido."
    )

    st.divider()

    # ==========================================
    # CONTROLE DO MÊS
    # ==========================================

    chave_mes = "calendario_locatario_mes"

    if chave_mes not in st.session_state:
        hoje = date.today()
        st.session_state[chave_mes] = date(
            hoje.year, hoje.month, 1
        )

    mes_atual = st.session_state[chave_mes]

    col_anterior, col_titulo, col_proximo, col_hoje = st.columns(
    [1.5, 3, 1.5, 1],
    gap="small",
    vertical_alignment="center",
)

    with col_anterior:
        if st.button(
            "‹ Anterior",
            key="calendario_locatario_anterior",
        ):
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
            f"{MESES[mes_atual.month - 1].capitalize()} "
            f"de {mes_atual.year}"
            "</h3>",
            unsafe_allow_html=True,
        )

    with col_proximo:
        if st.button(
            "Próximo ›",
            key="calendario_locatario_proximo",
        ):
            ano = mes_atual.year
            mes = mes_atual.month + 1

            if mes == 13:
                ano += 1
                mes = 1

            st.session_state[chave_mes] = date(ano, mes, 1)
            st.rerun()

    with col_hoje:
        if st.button(
            "Hoje",
            key="calendario_locatario_hoje",
            use_container_width=True,
        ):
            hoje = date.today()
            st.session_state[chave_mes] = date(
                hoje.year, hoje.month, 1
            )
            st.rerun()

    # ==========================================
    # BUSCAR RESERVAS DO USUÁRIO
    # ==========================================

    try:
        reservas = reservas_de(usuario["nome"])
    except Exception as erro:
        st.error(
            f"Não foi possível carregar suas reservas: {erro}"
        )
        return

    # Mostrar somente reservas confirmadas
    reservas_confirmadas = [
        reserva
        for reserva in reservas
        if reserva.get("status") == "Confirmada"
    ]

    # ==========================================
    # ORGANIZAR RESERVAS POR DATA
    # ==========================================

    reservas_por_data = {}

    for reserva in reservas_confirmadas:
        data_reserva = reserva.get("data")

        if not data_reserva:
            continue

        try:
            data_formatada = datetime.strptime(
                data_reserva, "%d/%m/%Y"
            ).date().isoformat()

        except (ValueError, TypeError):
            continue

        reservas_por_data.setdefault(
            data_formatada, []
        ).append(reserva)

    for lista in reservas_por_data.values():
        lista.sort(
            key=lambda item: item.get("horario", "")
        )

    st.caption(
        "O calendário mostra apenas reservas "
        "aprovadas/confirmadas."
    )

    st.markdown(
    """
    <div style="
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 15px;
    ">
        ✓ Reserva confirmada
    </div>
    """,
    unsafe_allow_html=True,
)

    # ==========================================
    # CABEÇALHO DOS DIAS DA SEMANA
    # ==========================================

    cabecalho = st.columns(7, gap="small")

    for coluna, nome_dia in zip(
        cabecalho, DIAS_SEMANA
    ):
        with coluna:
            st.markdown(
                "<p style='text-align:center; "
                "font-weight:600;'>"
                f"{nome_dia}</p>",
                unsafe_allow_html=True,
            )

    # ==========================================
    # GERAR CALENDÁRIO
    # ==========================================

    calendario_mes = calendar.Calendar(
        firstweekday=0
    )

    semanas = calendario_mes.monthdayscalendar(
        mes_atual.year,
        mes_atual.month,
    )

    hoje = date.today()

    for semana in semanas:
        colunas = st.columns(7, gap="small")

        for coluna, numero_dia in zip(
            colunas, semana
        ):
            with coluna:

                if numero_dia == 0:
                    st.markdown(
                        "&nbsp;",
                        unsafe_allow_html=True,
                    )
                    continue

                data_iso = date(
                    mes_atual.year,
                    mes_atual.month,
                    numero_dia,
                ).isoformat()

                # ==================================
                # QUADRADO DO DIA
                # ==================================

                with st.container(
                    border=True,
                    height=110,
                ):

                    # Verificar se é o dia atual
                    eh_hoje = (
                        mes_atual.year == hoje.year
                        and mes_atual.month == hoje.month
                        and numero_dia == hoje.day
                    )

                    estilo_dia = (
                        "font-size:16px; "
                        "font-weight:700; "
                        "margin-bottom:8px; "
                        "text-align:center;"
                    )

                    if eh_hoje:
                        estilo_dia += (
                            "background-color:#DBEAFE; "
                            "color:#1D4ED8; "
                            "border-radius:8px; "
                            "padding:5px;"
                        )

                    st.markdown(
                        f"<div style='{estilo_dia}'>"
                        f"{numero_dia}</div>",
                        unsafe_allow_html=True,
                    )

                    # ==================================
                    # RESERVAS DO DIA
                    # ==================================

                    eventos = reservas_por_data.get(
                        data_iso, []
                    )

                    if not eventos:
                        continue

                    for reserva in eventos:

                        horario = reserva.get(
                            "horario",
                            "Horário não informado",
                        )

                        # Buscar detalhes da sala
                        try:
                            detalhes_sala = sala_por_id(
                                reserva.get("sala_id")
                            )

                            sala = detalhes_sala.get(
                                "nome", "Sala"
                            )

                        except (
                            StopIteration,
                            ValueError,
                            TypeError,
                            KeyError,
                        ):
                            detalhes_sala = None
                            sala = "Sala não encontrada"

                        st.markdown(
    f"""
    <div style="
        background-color: #DCFCE7;
        color: #166534;
        border-radius: 6px;
        padding: 5px;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 5px;
    ">
        ✓ {horario}
<div style="font-size:11px; margin-top:3px;">
    {sala}
</div>
    </div>
    """,
    unsafe_allow_html=True,
)

                        # ==================================
                        # DETALHES DA RESERVA
                        # ==================================

                        with st.expander(
                            f"🏢 {sala} · Ver detalhes",
                            expanded=False,
                        ):

                            st.write(
                                f"**Horário:** {horario}"
                            )

                            st.write(
                                "**Status:** Confirmada"
                            )

                            if detalhes_sala:

                                st.write(
                                    "**Capacidade:** "
                                    f"{detalhes_sala.get('capacidade', '—')} "
                                    "pessoas"
                                )

                                localizacao = (
                                    detalhes_sala.get("andar")
                                    or detalhes_sala.get("localizacao")
                                    or "Não informada"
                                )

                                st.write(
                                    "**Localização:** "
                                    f"{localizacao}"
                                )

                                recursos = [
                                    rotulo
                                    for chave, rotulo
                                    in MAPA_RECURSOS
                                    if detalhes_sala.get(chave)
                                ]

                                st.write(
                                    "**Recursos:** "
                                    + (
                                        ", ".join(recursos)
                                        if recursos
                                        else "Nenhum informado"
                                    )
                                )

                            else:
                                st.caption(
                                    "Os detalhes completos "
                                    "desta sala não estão "
                                    "disponíveis."
                                )

    # ==========================================
    # MENSAGEM SEM RESERVAS
    # ==========================================

    if not reservas_confirmadas:
        st.info(
            "Você ainda não tem reservas "
            "confirmadas neste calendário."
        )
