from datetime import date, time
import streamlit as st

from utils.estado import (
    sala_por_id, reservas_de, salas_de, reservas_das_salas, adicionar_sala,
    listar_usuarios_admin, alterar_tipo_usuario_admin,
    confirmar_email_manualmente_admin, excluir_usuario_admin,
    desativar_usuario_admin, ativar_usuario_admin,
    TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN,
)
from utils.componentes import render_card, render_secao_titulo, render_lista_reservas, render_sala_card
from controllers.autorizacao_controller import exigir_tipo


# ==========================================
# # PÁGINAS - LOCATÁRIO
# ==========================================

def pagina_dashboard_locatario(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(f'<div class="titulo">OlÃ¡, {usuario["nome"].split()[0]}! ðŸ‘‹</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Encontre uma sala para o seu proximo compromisso.</div>', unsafe_allow_html=True)

    minhas_reservas = reservas_de(usuario["nome"])
    hoje = "17/08/2026"
    reservas_hoje = [r for r in minhas_reservas if r["data"] == hoje]
    confirmadas_hoje = [r for r in reservas_hoje if r["status"] == "Confirmada"]
    proxima = minhas_reservas[0] if minhas_reservas else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_card("ðŸ“… Reservas hoje", len(reservas_hoje), f"{len(confirmadas_hoje)} confirmação(ões)")
    with col2:
        render_card("ðŸ¢ Salas cadastradas", len(st.session_state.salas), "No sistema")
    with col3:
        render_card("ðŸ“‹ Minhas reservas", len(minhas_reservas), "Total ativo")
    with col4:
        if proxima:
            sala = sala_por_id(proxima["sala_id"])
            render_card("â° Próxima reserva", proxima["horario"].split(" - ")[0], sala["nome"])
        else:
            render_card("â° Próxima reserva", "â€”", "Nenhuma agendada")

    if proxima:
        sala = sala_por_id(proxima["sala_id"])
        st.markdown(f"""
        <div class="secao">
            <div class="secao-titulo">ðŸ“… Minha próxima reserva</div>
            <div class="reserva">
                <div class="reserva-titulo">ðŸ¢ {sala['nome']}</div>
                <div class="reserva-info">
                    ðŸ“… {proxima['data']} &nbsp;&nbsp;|&nbsp;&nbsp;
                    â° {proxima['horario']} &nbsp;&nbsp;|&nbsp;&nbsp;
                    ðŸ‘¥ atÃ© {sala['capacidade']} pessoas
                </div>
                <div class="reserva-info">ðŸ“ {sala['andar']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_secao_titulo("ðŸ“‹ Minhas próximas reservas")
    render_lista_reservas(minhas_reservas)


def pagina_buscar_salas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown('<div class="titulo">Buscar Salas ðŸ”Ž</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Filtre por data, horário e capacidade.</div>', unsafe_allow_html=True)

    render_secao_titulo("ðŸ”Ž Encontre uma sala disponívél")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_busca = st.date_input("Data", value=date(2026, 8, 17))
    with col2:
        horario_inicio = st.time_input("Horário inicial", value=time(9, 0))
    with col3:
        horario_fim = st.time_input("Horário final", value=time(10, 0))
    with col4:
        pessoas = st.number_input("Quantidade de pessoas", min_value=1, value=4)

    if st.button("ðŸ”Ž Procurar salas", type="primary"):
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
            st.success(f"Encontramos {len(resultado)} sala(s) disponívél(is)!")
            colunas = st.columns(3)
            for idx, sala in enumerate(resultado):
                render_sala_card(sala, colunas[idx % 3], contexto="busca", usuario_atual_nome=usuario["nome"])
        else:
            st.warning("Nenhuma sala livre para esses critérios. Tente outro horário ou capacidade.")


def pagina_minhas_reservas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown('<div class="titulo">Minhas Reservas ðŸ“…</div>', unsafe_allow_html=True)
    render_secao_titulo("ðŸ“‹ Todas as suas reservas")
    render_lista_reservas(reservas_de(usuario["nome"]))


def pagina_favoritos(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown('<div class="titulo">Favoritos â¤ï¸</div>', unsafe_allow_html=True)
    favoritas = [s for s in st.session_state.salas if s["id"] in st.session_state.favoritos]

    if not favoritas:
        st.caption("Voce ainda nao favoritou nenhuma sala. Vá em 'Buscar Salas' e clique no coração ðŸ¤.")
        return

    render_secao_titulo("â¤ï¸ Salas favoritas")
    colunas = st.columns(3)
    for idx, sala in enumerate(favoritas):
        render_sala_card(sala, colunas[idx % 3], contexto="favoritos", usuario_atual_nome=usuario["nome"])


def pagina_perfil(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown('<div class="titulo">Meu Perfil ðŸ‘¤</div>', unsafe_allow_html=True)
    render_secao_titulo("Dados do usuario")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")
    st.write(f"**Total de reservas:** {len(reservas_de(usuario['nome']))}")
    st.write(f"**Salas favoritas:** {len(st.session_state.favoritos)}")


# ==========================================
# PAGINAS - PROPRIETÁRIO
# ==========================================

def pagina_dashboard_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(f'<div class="titulo">Olá, {usuario["nome"].split()[0]}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Acompanhe suas salas e reservas.</div>', unsafe_allow_html=True)

    minhas_salas = salas_de(usuario["login"])
    minhas_salas_ids = [s["id"] for s in minhas_salas]
    reservas_recebidas = reservas_das_salas(minhas_salas_ids)
    confirmadas = len([r for r in reservas_recebidas if r["status"] == "Confirmada"])
    taxa = round(100 * confirmadas / len(reservas_recebidas)) if reservas_recebidas else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_card("ðŸ¢ Salas cadastradas", len(minhas_salas), "Salas ativas")
    with col2:
        render_card("ðŸ“… Reservas recebidas", len(reservas_recebidas), f"{confirmadas} confirmadas")
    with col3:
        render_card("ðŸ’° Faturamento", "R$ 2.450", "Este mês")
    with col4:
        render_card("ðŸ“Š Taxa de confirmação", f"{taxa}%", "Sobre reservas recebidas")

    render_secao_titulo("ðŸ“Š Resumo de ocupaçào")
    st.line_chart({"Semana 1": 45, "Semana 2": 62, "Semana 3": 55, "Semana 4": 72})

    render_secao_titulo("ðŸ“‹ Reservas recentes nas suas salas")
    render_lista_reservas(reservas_recebidas, mostrar_cliente=True)

    st.markdown("---")
    with st.expander("âž• Cadastrar nova sala"):
        with st.form("form_nova_sala", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da sala")
                capacidade = st.number_input("Capacidade", min_value=1, value=4)
            with col2:
                localizacao = st.text_input("Localização (ex: 2º andar)")

            st.caption("Recursos disponí­veis")
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
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown('<div class="titulo">Minhas Salas ðŸ¢</div>', unsafe_allow_html=True)
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
                <div class="sala-titulo">ðŸ¢ {sala['nome']}</div>
                <div class="sala-info">ðŸ‘¥ Capacidade: {sala['capacidade']} pessoas</div>
                <div class="sala-info">ðŸ–¥ï¸ {sala['recursos']}</div>
                <div class="sala-info">ðŸ“ {sala['andar']}</div>
            </div>
            """, unsafe_allow_html=True)


def pagina_perfil_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown('<div class="titulo">Meu Perfil ðŸ‘¤</div>', unsafe_allow_html=True)
    render_secao_titulo("Dados do usuário")
    st.write(f"**Nome:** {usuario['nome']}")
    st.write(f"**Tipo de conta:** {usuario['tipo']}")
    st.write(f"**Salas cadastradas:** {len(salas_de(usuario['login']))}")


# ==========================================
# PÁGINAS - ADMINISTRADOR
# ==========================================

def pagina_admin(usuario):
    exigir_tipo(usuario, [TIPO_ADMIN])

    st.markdown('<div class="titulo">Administração ðŸ› ï¸</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo">Gerencie as contas cadastradas no sistema.</div>',
        unsafe_allow_html=True,
    )

    usuarios = listar_usuarios_admin()

    col1, col2, col3 = st.columns(3)
    with col1:
        render_card("ðŸ‘¥ Total de contas", len(usuarios), "No sistema")
    with col2:
        confirmadas = len([u for u in usuarios if u["email_confirmado"]])
        render_card("âœ… E-mails confirmados", confirmadas, f"de {len(usuarios)}")
    with col3:
        admins = len([u for u in usuarios if u["tipo"] == TIPO_ADMIN])
        render_card("ðŸ› ï¸ Administradores", admins, "Contas com acesso total")

    render_secao_titulo("ðŸ‘¥ Contas cadastradas")

    for dados in usuarios:
        cols = st.columns([2, 2, 1.2, 1.2, 1.2, 1, 1])
        with cols[0]:
            st.write(f"**{dados['nome_completo'] or dados['nome_usuario']}**")
            st.caption(f"@{dados['nome_usuario']}")
        with cols[1]:
            st.write(dados["email"])
        with cols[2]:
            st.write("âœ… Confirmado" if dados["email_confirmado"] else "â³ Pendente")
            st.caption("ðŸ”“ Ativo" if dados["ativo"] else "ðŸ”’ Bloqueado")
        with cols[3]:
            novo_tipo = st.selectbox(
                "Tipo", [TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN],
                index=[TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN].index(dados["tipo"]),
                key=f"tipo_{dados['id']}", label_visibility="collapsed",
            )
            if novo_tipo != dados["tipo"]:
                alterar_tipo_usuario_admin(dados["id"], novo_tipo)
                st.rerun()
        with cols[4]:
            if not dados["email_confirmado"]:
                if st.button("Confirmar", key=f"confirmar_{dados['id']}"):
                    confirmar_email_manualmente_admin(dados["id"])
                    st.rerun()
        with cols[5]:
            if dados["id"] != usuario["id"]:
                if dados["ativo"]:
                    if st.button("ðŸ”’ Bloquear", key=f"bloquear_{dados['id']}"):
                        desativar_usuario_admin(dados["id"])
                        st.rerun()
                else:
                    if st.button("ðŸ”“ Reativar", key=f"reativar_{dados['id']}"):
                        ativar_usuario_admin(dados["id"])
                        st.rerun()
        with cols[6]:
            if dados["id"] != usuario["id"]:
                if st.button("ðŸ—‘ï¸", key=f"excluir_{dados['id']}"):
                    excluir_usuario_admin(dados["id"])
                    st.rerun()
        st.divider()




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
    "Perfil": pagina_perfil_proprietario,
}

# O administrador tem acesso total: todas as páginas de proprietário
# (para poder gerenciar salas do sistema) mais o painel de contas.
PAGINAS_ADMIN = {
    **PAGINAS_PROPRIETARIO,
    "ðŸ› ï¸ Administração": pagina_admin,
}

PAGINAS_POR_TIPO = {
    TIPO_LOCATARIO: PAGINAS_LOCATARIO,
    TIPO_PROPRIETARIO: PAGINAS_PROPRIETARIO,
    TIPO_ADMIN: PAGINAS_ADMIN,
}


def menu_para(tipo_usuario):
    """app.py usa isso para saber quais itens mostrar no menu,
    já que cada tipo de conta tem paginas diferentes."""
    paginas = PAGINAS_POR_TIPO.get(tipo_usuario, PAGINAS_LOCATARIO)
    return list(paginas.keys())


def render_pagina(pagina, usuario):
    paginas = PAGINAS_POR_TIPO.get(usuario["tipo"], PAGINAS_LOCATARIO)
    funcao = paginas.get(pagina, next(iter(paginas.values())))
    funcao(usuario)

