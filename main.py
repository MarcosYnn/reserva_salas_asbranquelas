from datetime import date, time
import streamlit as st

from estado import sala_por_id, reservas_de, salas_de, reservas_das_salas, adicionar_sala
from componentes import render_card, render_secao_titulo, render_lista_reservas, render_sala_card


# ==========================================
# PÁGINAS - LOCATÁRIO
# ==========================================

def pagina_dashboard_locatario(usuario):
    st.markdown(f'<div class="titulo">Olá, {usuario["nome"].split()[0]}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Encontre uma sala para o seu próximo compromisso.</div>', unsafe_allow_html=True)

    minhas_reservas = reservas_de(usuario["nome"])
    hoje = "17/08/2026"
    reservas_hoje = [r for r in minhas_reservas if r["data"] == hoje]
    confirmadas_hoje = [r for r in reservas_hoje if r["status"] == "Confirmada"]
    proxima = minhas_reservas[0] if minhas_reservas else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_card("📅 Reservas hoje", len(reservas_hoje), f"{len(confirmadas_hoje)} confirmação(ões)")
    with col2:
        render_card("🏢 Salas cadastradas", len(st.session_state.salas), "No sistema")
    with col3:
        render_card("📋 Minhas reservas", len(minhas_reservas), "Total ativo")
    with col4:
        if proxima:
            sala = sala_por_id(proxima["sala_id"])
            render_card("⏰ Próxima reserva", proxima["horario"].split(" - ")[0], sala["nome"])
        else:
            render_card("⏰ Próxima reserva", "—", "Nenhuma agendada")

    if proxima:
        sala = sala_por_id(proxima["sala_id"])
        st.markdown(f"""
        <div class="secao">
            <div class="secao-titulo">📅 Minha próxima reserva</div>
            <div class="reserva">
                <div class="reserva-titulo">🏢 {sala['nome']}</div>
                <div class="reserva-info">
                    📅 {proxima['data']} &nbsp;&nbsp;|&nbsp;&nbsp;
                    ⏰ {proxima['horario']} &nbsp;&nbsp;|&nbsp;&nbsp;
                    👥 até {sala['capacidade']} pessoas
                </div>
                <div class="reserva-info">📍 {sala['andar']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_secao_titulo("📋 Minhas próximas reservas")
    render_lista_reservas(minhas_reservas)


def pagina_buscar_salas(usuario):
    st.markdown('<div class="titulo">Buscar Salas 🔎</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Filtre por data, horário e capacidade.</div>', unsafe_allow_html=True)

    render_secao_titulo("🔎 Encontre uma sala disponível")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_busca = st.date_input("Data", value=date(2026, 8, 17))
    with col2:
        horario_inicio = st.time_input("Horário inicial", value=time(9, 0))
    with col3:
        horario_fim = st.time_input("Horário final", value=time(10, 0))
    with col4:
        pessoas = st.number_input("Quantidade de pessoas", min_value=1, value=4)

    if st.button("🔎 Procurar salas", type="primary"):
        st.session_state.busca_data_fmt = data_busca.strftime("%d/%m/%Y")
        st.session_state.busca_horario_fmt = f"{horario_inicio.strftime('%H:%M')} - {horario_fim.strftime('%H:%M')}"

        ocupadas_no_horario = {
            r["sala_id"] for r in st.session_state.reservas
            if r["data"] == st.session_state.busca_data_fmt
            and r["horario"] == st.session_state.busca_horario_fmt
        }

        st.session_state.resultado_busca = [
            s for s in st.session_state.salas
            if s["capacidade"] >= pessoas and s["id"] not in ocupadas_no_horario
        ]

    resultado = st.session_state.resultado_busca
    if resultado is not None:
        if resultado:
            st.success(f"Encontramos {len(resultado)} sala(s) disponível(is)!")
            colunas = st.columns(3)
            for idx, sala in enumerate(resultado):
                render_sala_card(sala, colunas[idx % 3], contexto="busca", usuario_atual_nome=usuario["nome"])
        else:
            st.warning("Nenhuma sala livre para esses critérios. Tente outro horário ou capacidade.")


def pagina_minhas_reservas(usuario):
    st.markdown('<div class="titulo">Minhas Reservas 📅</div>', unsafe_allow_html=True)
    render_secao_titulo("📋 Todas as suas reservas")
    render_lista_reservas(reservas_de(usuario["nome"]))


def pagina_favoritos(usuario):
    st.markdown('<div class="titulo">Favoritos ❤️</div>', unsafe_allow_html=True)
    favoritas = [s for s in st.session_state.salas if s["id"] in st.session_state.favoritos]

    if not favoritas:
        st.caption("Você ainda não favoritou nenhuma sala. Vá em 'Buscar Salas' e clique no coração 🤍.")
        return

    render_secao_titulo("❤️ Salas favoritas")
    colunas = st.columns(3)
    for idx, sala in enumerate(favoritas):
        render_sala_card(sala, colunas[idx % 3], contexto="favoritos", usuario_atual_nome=usuario["nome"])


def pagina_perfil(usuario):
    st.markdown('<div class="titulo">Meu Perfil 👤</div>', unsafe_allow_html=True)
    render_secao_titulo("Dados do usuário")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")
    st.write(f"**Total de reservas:** {len(reservas_de(usuario['nome']))}")
    st.write(f"**Salas favoritas:** {len(st.session_state.favoritos)}")


# ==========================================
# PÁGINAS - PROPRIETÁRIO
# ==========================================

def pagina_dashboard_proprietario(usuario):
    st.markdown(f'<div class="titulo">Olá, {usuario["nome"].split()[0]}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Acompanhe suas salas e reservas.</div>', unsafe_allow_html=True)

    minhas_salas = salas_de(usuario["login"])
    minhas_salas_ids = [s["id"] for s in minhas_salas]
    reservas_recebidas = reservas_das_salas(minhas_salas_ids)
    confirmadas = len([r for r in reservas_recebidas if r["status"] == "Confirmada"])
    taxa = round(100 * confirmadas / len(reservas_recebidas)) if reservas_recebidas else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_card("🏢 Salas cadastradas", len(minhas_salas), "Salas ativas")
    with col2:
        render_card("📅 Reservas recebidas", len(reservas_recebidas), f"{confirmadas} confirmadas")
    with col3:
        render_card("💰 Faturamento", "R$ 2.450", "Este mês")
    with col4:
        render_card("📊 Taxa de confirmação", f"{taxa}%", "Sobre reservas recebidas")

    render_secao_titulo("📊 Resumo de ocupação")
    st.line_chart({"Semana 1": 45, "Semana 2": 62, "Semana 3": 55, "Semana 4": 72})

    render_secao_titulo("📋 Reservas recentes nas suas salas")
    render_lista_reservas(reservas_recebidas, mostrar_cliente=True)

    st.markdown("---")
    with st.expander("➕ Cadastrar nova sala"):
        with st.form("form_nova_sala", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da sala")
                capacidade = st.number_input("Capacidade", min_value=1, value=4)
            with col2:
                localizacao = st.text_input("Localização (ex: 2º andar)")

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

            salvar = st.form_submit_button("Salvar sala", type="primary")

        if salvar:
            if not nome.strip():
                st.error("Informe o nome da sala.")
            else:
                recursos_marcados = [
                    chave for chave, marcado in {
                        "projetor": projetor,
                        "computador": computador,
                        "internet": internet,
                        "webcam": webcam,
                        "quadro": quadro,
                        "ar_condicionado": ar_condicionado,
                    }.items() if marcado
                ]
                adicionar_sala(
                    nome=nome.strip(),
                    capacidade=capacidade,
                    localizacao=localizacao.strip(),
                    proprietario=usuario["login"],
                    recursos_marcados=recursos_marcados,
                )
                st.success(f"Sala '{nome}' cadastrada com sucesso!")
                st.rerun()


def pagina_minhas_salas(usuario):
    st.markdown('<div class="titulo">Minhas Salas 🏢</div>', unsafe_allow_html=True)
    render_secao_titulo("Salas cadastradas por você")

    minhas_salas = salas_de(usuario["login"])
    if not minhas_salas:
        st.caption("Você ainda não cadastrou nenhuma sala.")
        return

    colunas = st.columns(3)
    for idx, sala in enumerate(minhas_salas):
        with colunas[idx % 3]:
            st.markdown(f"""
            <div class="sala">
                <div class="sala-titulo">🏢 {sala['nome']}</div>
                <div class="sala-info">👥 Capacidade: {sala['capacidade']} pessoas</div>
                <div class="sala-info">🖥️ {sala['recursos']}</div>
                <div class="sala-info">📍 {sala['andar']}</div>
            </div>
            """, unsafe_allow_html=True)


def pagina_perfil_proprietario(usuario):
    st.markdown('<div class="titulo">Meu Perfil 👤</div>', unsafe_allow_html=True)
    render_secao_titulo("Dados do usuário")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")
    st.write(f"**Salas cadastradas:** {len(salas_de(usuario['login']))}")


# ==========================================
# ROTEAMENTO
# ==========================================
# app.py chama render_pagina(pagina, usuario) a cada rerun,
# repassando o que foi escolhido no menu lateral.

PAGINAS_LOCATARIO = {
    "🏠 Dashboard": pagina_dashboard_locatario,
    "🔎 Buscar Salas": pagina_buscar_salas,
    "📅 Minhas Reservas": pagina_minhas_reservas,
    "❤️ Favoritos": pagina_favoritos,
    "👤 Perfil": pagina_perfil,
}

PAGINAS_PROPRIETARIO = {
    "🏠 Dashboard": pagina_dashboard_proprietario,
    "🏢 Minhas Salas": pagina_minhas_salas,
    "👤 Perfil": pagina_perfil_proprietario,
}


def menu_para(tipo_usuario):
    """app.py usa isso para saber quais itens mostrar no menu,
    já que Locatário e Proprietário têm páginas diferentes."""
    if tipo_usuario == "Locatário":
        return list(PAGINAS_LOCATARIO.keys())
    return list(PAGINAS_PROPRIETARIO.keys())


def render_pagina(pagina, usuario):
    paginas = PAGINAS_LOCATARIO if usuario["tipo"] == "Locatário" else PAGINAS_PROPRIETARIO
    funcao = paginas.get(pagina, paginas["🏠 Dashboard"])
    funcao(usuario)