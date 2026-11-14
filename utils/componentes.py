import streamlit as st

from controllers.reserva_controller import criar_pedido_reserva
from models import reserva_firebase_model as reserva_model
from utils.estado import sala_por_id


def injetar_css():
    st.markdown("""
    <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: #f7f8fc !important;
            color: #15182f !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMain"] p,
        [data-testid="stMain"] span,
        [data-testid="stMain"] label,
        [data-testid="stMain"] h1,
        [data-testid="stMain"] h2,
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4,
        [data-testid="stMain"] h5,
        [data-testid="stMain"] h6,
        [data-testid="stMain"] div[data-testid="stMarkdownContainer"] {
            color: #15182f;
        }

        [data-testid="stMain"] input,
        [data-testid="stMain"] textarea,
        [data-testid="stMain"] [data-baseweb="select"] > div,
        [data-testid="stMain"] [data-baseweb="input"] > div {
            background-color: #ffffff !important;
            color: #15182f !important;
        }

        [data-testid="stMain"] input::placeholder,
        [data-testid="stMain"] textarea::placeholder {
            color: #6b7280 !important;
            opacity: 1 !important;
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {
            color: #15182f !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #171a4a 0%, #272c70 100%);
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        .titulo {
            font-size: 32px;
            font-weight: 700;
            color: #15182f !important;
            margin-bottom: 5px;
        }

        .subtitulo {
            font-size: 16px;
            color: #6b7280 !important;
            margin-bottom: 25px;
        }

        .card {
            background-color: white;
            border-radius: 14px;
            padding: 20px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            min-height: 120px;
        }

        .card-titulo {
            color: #6b7280 !important;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .card-numero {
            font-size: 28px;
            font-weight: 700;
            color: #15182f !important;
        }

        .card-info {
            color: #15805a !important;
            font-size: 13px;
            margin-top: 5px;
        }

        .secao {
            background-color: white;
            border-radius: 14px;
            padding: 22px;
            border: 1px solid #e5e7eb;
            margin-top: 20px;
        }

        .secao-titulo {
            font-size: 20px;
            font-weight: 700;
            color: #15182f !important;
            margin-bottom: 18px;
        }

        .reserva {
            background-color: #fafbff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }

        .reserva-titulo {
            font-weight: 700;
            color: #15182f !important;
        }

        .reserva-info {
            color: #4b5563 !important;
            font-size: 14px;
            margin-top: 5px;
        }

        .sala {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 10px;
        }

        .sala-titulo {
            font-size: 18px;
            font-weight: 700;
            color: #15182f !important;
        }

        .sala-info {
            color: #4b5563 !important;
            font-size: 14px;
            margin-top: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_card(titulo, numero, info):
    st.markdown(f"""
    <div class="card">
        <div class="card-titulo">{titulo}</div>
        <div class="card-numero">{numero}</div>
        <div class="card-info">{info}</div>
    </div>
    """, unsafe_allow_html=True)


def render_secao_titulo(texto):
    st.markdown(f"""
    <div class="secao">
        <div class="secao-titulo">{texto}</div>
    </div>
    """, unsafe_allow_html=True)


def render_lista_reservas(
    lista,
    mostrar_cliente=False,
    permitir_cancelar=False,
):
    if not lista:
        st.caption("Nenhuma reserva encontrada.")
        return

    for indice, reserva in enumerate(lista):
        try:
            sala = sala_por_id(reserva["sala_id"])
        except (StopIteration, ValueError, KeyError):
            sala = None

        nome_sala = (
            sala["nome"]
            if sala
            else reserva.get("sala_nome", "Sala")
        )

        colunas = st.columns(
            [2, 2, 1.2, 1.5, 1]
            if mostrar_cliente
            else [2, 1.2, 1.5, 1]
        )

        with colunas[0]:
            st.write(f"**{nome_sala}**")

        posicao = 1
        if mostrar_cliente:
            with colunas[posicao]:
                st.write(reserva.get("solicitante_nome", "—"))
            posicao += 1

        with colunas[posicao]:
            st.write(reserva.get("data", "—"))

        with colunas[posicao + 1]:
            horario = (
                f"{reserva.get('hora_inicio', '—')} - "
                f"{reserva.get('hora_fim', '—')}"
            )
            st.write(horario)

        with colunas[posicao + 2]:
            status = reserva.get("status", "Pendente")
            if status == reserva_model.APROVADA:
                st.success(status)
            elif status == reserva_model.RECUSADA:
                st.error(status)
            elif status == reserva_model.CANCELADA:
                st.caption(status)
            else:
                st.warning(status)


def render_sala_card(
    sala,
    coluna,
    contexto,
    usuario_atual,
):
    with coluna:
        favoritada = sala["id"] in st.session_state.favoritos

        st.markdown(f"""
        <div class="sala">
            <div class="sala-titulo">🏢 {sala['nome']}</div>
            <div class="sala-info">
                👥 Capacidade: {sala['capacidade']} pessoas
            </div>
            <div class="sala-info">🖥️ {sala['recursos']}</div>
            <div class="sala-info">📍 {sala['andar']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_reservar, col_fav = st.columns([2, 1])

        with col_reservar:
            if st.button(
                "Reservar",
                key=f"reservar_{contexto}_{sala['id']}",
            ):
                data = st.session_state.get("busca_data_iso")
                hora_inicio = st.session_state.get("busca_hora_inicio")
                hora_fim = st.session_state.get("busca_hora_fim")

                try:
                    criar_pedido_reserva(
                        usuario_atual=usuario_atual,
                        sala=sala,
                        data=data,
                        hora_inicio=hora_inicio,
                        hora_fim=hora_fim,
                    )
                    st.success(
                        "Pedido enviado. O status inicial é Pendente."
                    )
                    st.rerun()
                except Exception as erro:
                    st.error(f"Não foi possível criar o pedido: {erro}")

        with col_fav:
            rotulo = (
                "Remover"
                if contexto == "favoritos"
                else ("💛" if favoritada else "🤍")
            )

            if st.button(
                rotulo,
                key=f"fav_{contexto}_{sala['id']}",
            ):
                if favoritada:
                    st.session_state.favoritos.discard(sala["id"])
                else:
                    st.session_state.favoritos.add(sala["id"])
                st.rerun()