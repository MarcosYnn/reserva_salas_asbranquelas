from datetime import date, datetime, time

import streamlit as st

from controllers.autorizacao_controller import exigir_tipo
from controllers.reserva_controller import (
    listar_reservas_ativas_para_busca,
    listar_reservas_usuario,
)
from utils.componentes import (
    render_card,
    render_secao_titulo,
    render_sala_card,
)
from utils.estado import (
    TIPO_ADMIN,
    TIPO_LOCATARIO,
    TIPO_PROPRIETARIO,
    adicionar_sala,
    sala_por_id,
    salas_de,
)
from views.admin_view import renderizar_admin_usuarios
from views.reserva_view import renderizar_reservas


def _formatar_data(data_iso):
    try:
        return date.fromisoformat(data_iso).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return data_iso or "—"


# ==========================================
# PÁGINAS — LOCATÁRIO
# ==========================================

def pagina_dashboard_locatario(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        f'<div class="titulo">Olá, {usuario["nome"].split()[0]}! 👋</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitulo">'
        "Encontre uma sala para o seu próximo compromisso."
        "</div>",
        unsafe_allow_html=True,
    )

    try:
        minhas_reservas = listar_reservas_usuario(usuario)
    except Exception as erro:
        st.error(f"Não foi possível carregar suas reservas: {erro}")
        minhas_reservas = []

    hoje = date.today().isoformat()
    reservas_hoje = [
        reserva
        for reserva in minhas_reservas
        if reserva.get("data") == hoje
    ]
    aprovadas_hoje = [
        reserva
        for reserva in reservas_hoje
        if reserva.get("status") == "Aprovada"
    ]

    reservas_ativas = [
        reserva
        for reserva in minhas_reservas
        if reserva.get("status") in {"Pendente", "Aprovada"}
        and reserva.get("data", "") >= hoje
    ]
    proxima = min(
        reservas_ativas,
        key=lambda reserva: (
            reserva.get("data", ""),
            reserva.get("hora_inicio", ""),
        ),
        default=None,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_card(
            "📅 Reservas hoje",
            len(reservas_hoje),
            f"{len(aprovadas_hoje)} aprovada(s)",
        )

    with col2:
        render_card(
            "🏢 Salas cadastradas",
            len(st.session_state.get("salas", [])),
            "No sistema",
        )

    with col3:
        render_card(
            "📋 Minhas reservas",
            len(minhas_reservas),
            "Total de pedidos",
        )

    with col4:
        if proxima:
            render_card(
                "⏰ Próxima reserva",
                proxima.get("hora_inicio", "—"),
                proxima.get("sala_nome", "Sala"),
            )
        else:
            render_card(
                "⏰ Próxima reserva",
                "—",
                "Nenhuma agendada",
            )

    st.subheader("Status das minhas reservas")
    renderizar_reservas(usuario)


def pagina_buscar_salas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="titulo">Buscar Salas 🔎</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitulo">'
        "Filtre por data, horário e capacidade."
        "</div>",
        unsafe_allow_html=True,
    )

    render_secao_titulo("🔎 Encontre uma sala disponível")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        data_busca = st.date_input(
            "Data",
            value=date.today(),
        )

    with col2:
        horario_inicio = st.time_input(
            "Horário inicial",
            value=time(9, 0),
        )

    with col3:
        horario_fim = st.time_input(
            "Horário final",
            value=time(10, 0),
        )

    with col4:
        pessoas = st.number_input(
            "Quantidade de pessoas",
            min_value=1,
            value=4,
        )

    if st.button("🔎 Procurar salas", type="primary"):
        if horario_fim <= horario_inicio:
            st.session_state.resultado_busca = []
            st.error("O horário final deve ser depois do horário inicial.")
        else:
            data_iso = data_busca.strftime("%Y-%m-%d")
            inicio_txt = horario_inicio.strftime("%H:%M")
            fim_txt = horario_fim.strftime("%H:%M")

            st.session_state.busca_data_iso = data_iso
            st.session_state.busca_hora_inicio = inicio_txt
            st.session_state.busca_hora_fim = fim_txt

            try:
                reservas_ativas = listar_reservas_ativas_para_busca(usuario)
            except Exception as erro:
                st.error(f"Não foi possível consultar reservas: {erro}")
                reservas_ativas = []

            salas_ocupadas = set()

            for reserva in reservas_ativas:
                if reserva.get("data") != data_iso:
                    continue

                inicio_reserva = reserva.get("hora_inicio", "")
                fim_reserva = reserva.get("hora_fim", "")

                # Considera indisponíveis os horários que se sobrepõem.
                if inicio_txt < fim_reserva and fim_txt > inicio_reserva:
                    salas_ocupadas.add(str(reserva.get("sala_id")))

            st.session_state.resultado_busca = [
                sala
                for sala in st.session_state.get("salas", [])
                if sala["capacidade"] >= pessoas
                and str(sala["id"]) not in salas_ocupadas
            ]

    resultado = st.session_state.get("resultado_busca")

    if resultado is not None:
        if resultado:
            st.success(
                f"Encontramos {len(resultado)} sala(s) disponível(is)!"
            )
            colunas = st.columns(3)

            for indice, sala in enumerate(resultado):
                render_sala_card(
                    sala=sala,
                    coluna=colunas[indice % 3],
                    contexto="busca",
                    usuario_atual=usuario,
                )
        else:
            st.warning(
                "Nenhuma sala livre para esses critérios. "
                "Tente outro horário ou capacidade."
            )


def pagina_minhas_reservas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="titulo">Minhas Reservas 📅</div>',
        unsafe_allow_html=True,
    )
    renderizar_reservas(usuario)


def pagina_favoritos(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="titulo">Favoritos ❤️</div>',
        unsafe_allow_html=True,
    )

    favoritas = [
        sala
        for sala in st.session_state.get("salas", [])
        if sala["id"] in st.session_state.get("favoritos", set())
    ]

    if not favoritas:
        st.caption(
            "Você ainda não favoritou nenhuma sala. "
            "Vá em 'Buscar Salas' e clique no coração."
        )
        return

    render_secao_titulo("❤️ Salas favoritas")
    colunas = st.columns(3)

    for indice, sala in enumerate(favoritas):
        render_sala_card(
            sala=sala,
            coluna=colunas[indice % 3],
            contexto="favoritos",
            usuario_atual=usuario,
        )


def pagina_perfil(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="titulo">Meu Perfil 👤</div>',
        unsafe_allow_html=True,
    )
    render_secao_titulo("Dados do usuário")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")

    try:
        total_reservas = len(listar_reservas_usuario(usuario))
    except Exception:
        total_reservas = 0

    st.write(f"**Total de reservas:** {total_reservas}")
    st.write(
        f"**Salas favoritas:** "
        f"{len(st.session_state.get('favoritos', set()))}"
    )


# ==========================================
# PÁGINAS — PROPRIETÁRIO
# ==========================================

def pagina_dashboard_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(
        f'<div class="titulo">Olá, '
        f'{usuario["nome"].split()[0]}! 👋</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitulo">'
        "Acompanhe suas salas e os pedidos recebidos."
        "</div>",
        unsafe_allow_html=True,
    )

    minhas_salas = salas_de(usuario["login"])

    try:
        reservas_recebidas = listar_reservas_usuario(usuario)
    except Exception as erro:
        st.error(f"Não foi possível carregar os pedidos: {erro}")
        reservas_recebidas = []

    pendentes = [
        reserva
        for reserva in reservas_recebidas
        if reserva.get("status") == "Pendente"
    ]
    aprovadas = [
        reserva
        for reserva in reservas_recebidas
        if reserva.get("status") == "Aprovada"
    ]

    taxa_aprovacao = (
        round(100 * len(aprovadas) / len(reservas_recebidas))
        if reservas_recebidas
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_card("Salas cadastradas", len(minhas_salas), "Nas suas salas")

    with col2:
        render_card(
            "Pedidos recebidos",
            len(reservas_recebidas),
            "Total",
        )

    with col3:
        render_card(
            "Pedidos pendentes",
            len(pendentes),
            "Aguardando decisão do administrador",
        )

    with col4:
        render_card(
            "Taxa aprovada",
            f"{taxa_aprovacao}%",
            "Sobre pedidos recebidos",
        )

    st.subheader("Pedidos para minhas salas")
    renderizar_reservas(usuario)

    st.markdown("---")

    with st.expander("Cadastrar nova sala"):
        with st.form("form_nova_sala", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome da sala")
                capacidade = st.number_input(
                    "Capacidade",
                    min_value=1,
                    value=4,
                )

            with col2:
                localizacao = st.text_input(
                    "Localização (ex: 2º andar)"
                )

            st.caption("Recursos disponíveis")
            rc1, rc2, rc3 = st.columns(3)

            with rc1:
                projetor = st.checkbox("Projetor")
                computador = st.checkbox("Computador")

            with rc2:
                internet = st.checkbox("Wi-Fi")
                webcam = st.checkbox("Webcam")

            with rc3:
                quadro = st.checkbox("Quadro branco")
                ar_condicionado = st.checkbox("Ar-condicionado")

            salvar = st.form_submit_button(
                "Salvar sala",
                type="primary",
            )

        if salvar:
            if not nome.strip():
                st.error("Informe o nome da sala.")
            else:
                recursos_marcados = [
                    chave
                    for chave, marcado in {
                        "projetor": projetor,
                        "computador": computador,
                        "internet": internet,
                        "webcam": webcam,
                        "quadro": quadro,
                        "ar_condicionado": ar_condicionado,
                    }.items()
                    if marcado
                ]

                try:
                    adicionar_sala(
                        nome=nome.strip(),
                        capacidade=capacidade,
                        localizacao=localizacao.strip(),
                        proprietario=usuario["login"],
                        recursos_marcados=recursos_marcados,
                    )
                    st.success(f"Sala '{nome}' cadastrada com sucesso!")
                    st.rerun()
                except Exception as erro:
                    st.error(f"Não foi possível cadastrar a sala: {erro}")


def pagina_minhas_salas(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(
        '<div class="titulo">Minhas Salas 🏢</div>',
        unsafe_allow_html=True,
    )
    render_secao_titulo("Salas cadastradas por você")

    minhas_salas = salas_de(usuario["login"])

    if not minhas_salas:
        st.caption("Você ainda não cadastrou nenhuma sala.")
        return

    colunas = st.columns(3)

    for indice, sala in enumerate(minhas_salas):
        with colunas[indice % 3]:
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


def pagina_pedidos_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(
        '<div class="titulo">Pedidos para minhas salas</div>',
        unsafe_allow_html=True,
    )
    renderizar_reservas(usuario)


def pagina_perfil_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(
        '<div class="titulo">Meu Perfil 👤</div>',
        unsafe_allow_html=True,
    )
    render_secao_titulo("Dados do usuário")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")
    st.write(f"**Salas cadastradas:** {len(salas_de(usuario['login']))}")


# ==========================================
# PÁGINAS — ADMINISTRADOR
# ==========================================

def pagina_admin(usuario):
    exigir_tipo(usuario, [TIPO_ADMIN])

    st.markdown(
        '<div class="titulo">Administração</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Pedidos de reserva")
    renderizar_reservas(usuario)

    st.divider()
    renderizar_admin_usuarios(usuario)


# ==========================================
# MENUS POR PERFIL
# ==========================================

PAGINAS_LOCATARIO = {
    "Dashboard": pagina_dashboard_locatario,
    "Buscar Salas": pagina_buscar_salas,
    "Minhas Reservas": pagina_minhas_reservas,
    "Favoritos": pagina_favoritos,
    "Perfil": pagina_perfil,
}

PAGINAS_PROPRIETARIO = {
    "Dashboard": pagina_dashboard_proprietario,
    "Minhas Salas": pagina_minhas_salas,
    "Pedidos de Reserva": pagina_pedidos_proprietario,
    "Perfil": pagina_perfil_proprietario,
}

PAGINAS_ADMIN = {
    **PAGINAS_PROPRIETARIO,
    "Administração": pagina_admin,
}

PAGINAS_POR_TIPO = {
    TIPO_LOCATARIO: PAGINAS_LOCATARIO,
    TIPO_PROPRIETARIO: PAGINAS_PROPRIETARIO,
    TIPO_ADMIN: PAGINAS_ADMIN,
}


def menu_para(tipo_usuario):
    paginas = PAGINAS_POR_TIPO.get(
        tipo_usuario,
        PAGINAS_LOCATARIO,
    )
    return list(paginas.keys())


def render_pagina(pagina, usuario):
    paginas = PAGINAS_POR_TIPO.get(
        usuario["tipo"],
        PAGINAS_LOCATARIO,
    )
    funcao = paginas.get(pagina, next(iter(paginas.values())))
    funcao(usuario)