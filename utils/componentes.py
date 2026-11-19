import streamlit as st

from html import escape

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

        [data-testid="stMain"] [data-testid="stButton"] button[kind="primary"] {
            border: 1px solid #2563eb;
            border-radius: 9px;
            background: #2563eb;
            color: #ffffff !important;
            font-weight: 600;
        }

        [data-testid="stMain"] [data-testid="stButton"] button[kind="primary"]:hover {
            border-color: #1d4ed8;
            background: #1d4ed8;
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {
            color: #15182f !important;
        }

        section[data-testid="stSidebar"] {
            background: #0b1120;
            border-right: 1px solid #182238;
        }

        section[data-testid="stSidebar"] * {
            color: #d8e1f0;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            margin-bottom: 0.25rem;
        }

        section[data-testid="stSidebar"] [data-testid="stButton"] button {
            width: 100%;
            min-height: 2.65rem;
            border: 1px solid transparent;
            border-radius: 9px;
            background: transparent;
            color: #91a1bb;
            text-align: left;
            justify-content: flex-start;
            padding: 0.55rem 0.75rem;
            font-weight: 500;
        }

        section[data-testid="stSidebar"] [data-testid="stButton"] button > div {
            width: 100%;
            justify-content: flex-start !important;
        }

        section[data-testid="stSidebar"] [data-testid="stButton"] button p {
            width: 100%;
            text-align: left !important;
        }

        section[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
            background: #17243a;
            border-color: #253652;
            color: #ffffff;
        }

        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
            background: #2563eb;
            color: #ffffff;
        }

        .app-brand {
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.25;
        }

        .app-brand small {
            display: block;
            margin-top: 0.2rem;
            color: #7f91ad;
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .app-menu-label {
            margin: 1.5rem 0 0.45rem;
            color: #71819a;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .app-user {
            padding: 0.75rem 0;
            border-top: 1px solid #202b3e;
            color: #ffffff;
            font-weight: 600;
        }

        .app-user small {
            display: block;
            margin-top: 0.2rem;
            color: #8b9ab2;
            font-size: 0.78rem;
            font-weight: 400;
        }

        .app-page-header {
            margin: -1.5rem -1rem 1.5rem;
            padding: 1rem 1.5rem 0.9rem;
            background: #ffffff;
            border-bottom: 1px solid #dce4ef;
        }

        .app-page-header h2 {
            margin: 0;
            color: #101b31;
            font-size: 1.25rem;
            font-weight: 700;
        }

        .app-page-header p {
            margin: 0.2rem 0 0;
            color: #71819a;
            font-size: 0.82rem;
        }

        @media (max-width: 768px) {
            .app-page-header { margin: -1rem -0.5rem 1rem; padding: 0.85rem 1rem; }
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

        .page-intro {
            margin: 0.15rem 0 1rem;
            color: #66758e;
            font-size: 0.92rem;
        }

        .search-section-heading {
            margin: 1.1rem 0 0.45rem;
            color: #13213a;
            font-size: 1.08rem;
            font-weight: 700;
        }

        .card {
            background-color: white;
            border-radius: 14px;
            padding: 19px;
            border: 1px solid #dce4ef;
            box-shadow: 0 2px 7px rgba(15, 35, 70, 0.035);
            min-height: 120px;
            transition: transform 140ms ease, box-shadow 140ms ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(15, 35, 70, 0.08);
        }

        .dashboard-hero {
            position: relative;
            overflow: hidden;
            margin-bottom: 1.25rem;
            padding: 1.65rem 1.8rem;
            border-radius: 16px;
            background: linear-gradient(115deg, #1e3a70 0%, #244b8f 100%);
            color: #ffffff;
        }

        .dashboard-hero::after {
            position: absolute;
            top: -4rem;
            right: -2rem;
            width: 14rem;
            height: 14rem;
            border: 1.4rem solid rgba(255, 255, 255, 0.055);
            border-radius: 50%;
            content: "";
            pointer-events: none;
        }

        .dashboard-hero-label {
            margin-bottom: 0.55rem;
            color: #9ccaff;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .dashboard-hero-title {
            display: block;
            margin: 0;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.3;
        }

        .dashboard-hero p {
            margin: 0.45rem 0 0;
            color: #d2e3ff;
            font-size: 0.94rem;
        }

        .dashboard-section-title {
            margin: 1.4rem 0 0.2rem;
            color: #13213a;
            font-size: 1.05rem;
            font-weight: 700;
        }

        .dashboard-section-caption {
            margin: 0 0 0.85rem;
            color: #71819a;
            font-size: 0.82rem;
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

        [data-testid="stExpander"] {
            margin: 0.5rem 0;
            overflow: hidden;
            border: 1px solid #dce4ef !important;
            border-radius: 10px !important;
            background: #ffffff;
        }

        [data-testid="stExpander"] summary {
            min-height: 2.6rem;
        }
    </style>
    """, unsafe_allow_html=True)


def renderizar_cabecalho_pagina(titulo, subtitulo="Sistema Acadêmico"):
    titulo_seguro = escape(str(titulo))
    subtitulo_seguro = escape(str(subtitulo))
    st.markdown(
        f'<div class="app-page-header"><h2>{titulo_seguro}</h2>'
        f'<p>{subtitulo_seguro}</p></div>',
        unsafe_allow_html=True,
    )


def renderizar_banner_dashboard(rotulo, nome, descricao):
    rotulo_seguro = escape(str(rotulo))
    nome_seguro = escape(str(nome))
    descricao_segura = escape(str(descricao))
    st.markdown(
        '<section class="dashboard-hero">'
        f'<div class="dashboard-hero-label">{rotulo_seguro}</div>'
        f'<div class="dashboard-hero-title" '
        f'style="color: #ffffff !important; -webkit-text-fill-color: #ffffff;">'
        f'Olá, {nome_seguro}!</div>'
        f'<p>{descricao_segura}</p>'
        '</section>',
        unsafe_allow_html=True,
    )


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

        nome = escape(str(sala.get("nome", "Sala")))
        capacidade = escape(str(sala.get("capacidade", "—")))
        recursos = escape(str(sala.get("recursos") or "Nenhum recurso informado"))
        andar = escape(str(sala.get("andar") or "Localização não informada"))

        with st.container(border=True):
            st.markdown(
                f"""
                <div style="padding: 0.25rem 0 0.8rem;">
                    <div style="
                        color: #13213a;
                        font-size: 1.05rem;
                        font-weight: 700;
                        margin-bottom: 0.7rem;
                    ">
                        🏢 {nome}
                    </div>
                    <div style="color: #52627a; margin-bottom: 0.45rem;">
                        👥 Capacidade: {capacidade} pessoas
                    </div>
                    <div style="color: #52627a; margin-bottom: 0.45rem;">
                        🖥️ {recursos}
                    </div>
                    <div style="color: #52627a;">
                        📍 {andar}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_reservar, col_favorito = st.columns([2, 1])

            with col_reservar:
                if st.button(
                    "Reservar",
                    key=f"reservar_{contexto}_{sala['id']}",
                    use_container_width=True,
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
                            necessita_equipamentos=st.session_state.get(
                                "busca_necessita_equipamentos",
                                False,
                            ),
                            evento_institucional=st.session_state.get(
                                "busca_evento_institucional",
                                False,
                            ),
                        )
                        st.success(
                            "Pedido enviado. O status inicial é Pendente."
                        )
                        st.rerun()
                    except Exception as erro:
                        st.error(
                            f"Não foi possível criar o pedido: {erro}"
                        )

            with col_favorito:
                rotulo = (
                    "Remover"
                    if contexto == "favoritos"
                    else ("♥" if favoritada else "♡")
                )

                if st.button(
                    rotulo,
                    key=f"fav_{contexto}_{sala['id']}",
                    use_container_width=True,
                ):
                    if favoritada:
                        st.session_state.favoritos.discard(sala["id"])
                    else:
                        st.session_state.favoritos.add(sala["id"])
                    st.rerun()
