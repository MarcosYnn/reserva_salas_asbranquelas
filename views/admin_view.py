from utils.relogio import hoje_local
import streamlit as st
from html import escape
from datetime import date, datetime


def mostrar_admin():
    """Painel administrativo do Sistema de Reserva de Salas."""
    if "admin_pagina" not in st.session_state:
        st.session_state.admin_pagina = "Início"

    # Sessões da navegação antiga guardavam a lista como uma seção do cadastro.
    secao_antiga = st.session_state.pop("admin_secao", None)
    if (
        st.session_state.admin_pagina == "Administração"
        and secao_antiga == "usuarios"
    ):
        st.session_state.admin_pagina = "Usuários cadastrados"

    def navegar(pagina):
        st.session_state.admin_pagina = pagina
        st.session_state.pop("admin_secao", None)
        st.rerun()

    st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background:#f6f8fc;}
[data-testid="stMainBlockContainer"] {max-width:100% !important;padding:0 1.5rem 2rem !important;}
#MainMenu, footer {display:none !important;}
[data-testid="stHeader"] {background:transparent !important;}
section[data-testid="stSidebar"] {background:#0b1120 !important;width:190px !important;min-width:190px !important;}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {padding:0.8rem 0.55rem !important;}
section[data-testid="stSidebar"] button[kind="secondary"] {background:transparent !important;color:#e2e9f6 !important;border:0 !important;text-align:left !important;justify-content:flex-start !important;font-size:12px !important;min-height:35px !important;}
section[data-testid="stSidebar"] button[kind="primary"] {background:#2563eb !important;color:white !important;border:0 !important;justify-content:flex-start !important;font-size:12px !important;min-height:35px !important;}
section[data-testid="stSidebar"] button:hover {background:#1e3355 !important;color:white !important;}
.sidebar-brand {color:#fff;font-size:13px;font-weight:750;padding:8px 4px 15px;border-bottom:1px solid #263146;margin-bottom:12px;}
.sidebar-brand small {display:block;font-size:9px;font-weight:400;letter-spacing:.5px;color:#7893bb;margin-top:4px;}
.sidebar-label {font-size:10px;color:#a5b8d6;letter-spacing:1px;margin:17px 4px 5px;}
.page-header {background:#fff;border-bottom:1px solid #e1e8f3;padding:15px 24px;margin:0 -1.5rem 0;color:#101c36;font-size:15px;font-weight:750;}
.page-header small {display:block;color:#7890ad;font-size:10px;font-weight:400;margin-top:4px;}
.admin-wrap {max-width:980px;margin:0 auto;padding:0 8px;}
.st-key-admin_hero_wrap {width:100% !important;max-width:none !important;margin:0 !important;padding:0 !important;}
.admin-hero {position:relative;overflow:hidden;background:#203d72;border-radius:0 0 13px 13px;color:#fff !important;padding:34px 28px 75px;min-height:215px;}
.admin-hero:before {content:"";position:absolute;border:25px solid #ffffff0a;width:160px;height:160px;border-radius:50%;right:-30px;top:-75px;}
.admin-hero:after {content:"";position:absolute;border:22px solid #ffffff0a;width:100px;height:100px;border-radius:50%;right:65px;bottom:-70px;}
.admin-hero .eyebrow {font-size:11px;letter-spacing:1.3px;font-weight:700;color:#bdd7ff !important;}
div.admin-hero h2, div.admin-hero h2 *, div.admin-hero h2 span {color:#ffffff !important;-webkit-text-fill-color:#ffffff !important;font-size:26px !important;font-weight:700 !important;line-height:1.3 !important;margin:15px 0 9px !important;}
.admin-hero p {font-size:14px !important;color:#e5efff !important;margin:0;line-height:1.6;}
/* Botão sobre o rodapé do mesmo banner, sem segunda faixa azul */
.st-key-hero_button {background:transparent !important;padding:0 !important;margin-top:-60px !important;margin-left:28px !important;margin-bottom:36px !important;position:relative !important;z-index:2;}
.st-key-hero_button [data-testid="stButton"] {width:128px !important;}
.st-key-hero_button [data-testid="stButton"] button {box-sizing:border-box !important;width:128px !important;height:42px !important;min-height:42px !important;padding:0 16px !important;background:#fff !important;color:#16335f !important;border:0 !important;border-radius:8px !important;font-size:12px !important;font-weight:700 !important;}
.st-key-hero_button button:hover {background:#e8f0ff !important;color:#16335f !important;}
.metric-card {background:white;border:1px solid #dce5f1;border-radius:11px;padding:13px;min-height:103px;}
.metric-icon {font-size:17px;color:#3275f6;display:block;margin-bottom:6px;}
.metric-card strong {display:block;color:#111c36;font-size:22px;line-height:1.1;}
.metric-card em {font-size:11px;color:#8ca0bd;font-style:normal;font-weight:400;}
.metric-card small {display:block;color:#7890af;font-size:10px;margin-top:4px;}
.section-title {font-size:14px;color:#10264a;font-weight:750;margin-top:18px;}
.section-hint {font-size:10px;color:#7890af;margin-bottom:10px;}
.action-card {background:white;border:1px solid #dce5f1;border-radius:11px;padding:12px;min-height:98px;}
.action-card .icon {display:inline-block;border-radius:8px;padding:5px 8px;background:#eff4fb;color:#3776f5;font-size:15px;}
.action-card h4 {font-size:11px;color:#132d54;margin:7px 0 3px;}
.action-card p {font-size:10px;color:#7589a7;line-height:1.45;margin:0;}
.st-key-actions button {font-size:10px !important;min-height:28px !important;margin-top:-3px !important;}
.mini-panel {background:white;border:1px solid #dce5f1;border-radius:11px;padding:13px;margin-bottom:12px;}
.mini-panel h4 {font-size:12px;color:#12294b;margin:0 0 9px;}
.mini-panel p {font-size:10px;color:#7187a6;margin:0;line-height:1.5;}
.reserve-line {font-size:10px;color:#19365c;padding:7px 0;border-bottom:1px solid #eef2f8;}
.reserve-line small {display:block;color:#8295af;font-size:9px;}
.bar-label {font-size:10px;color:#19345c;display:flex;justify-content:space-between;margin:8px 0 3px;}
.bar-track {height:4px;border-radius:4px;background:#e8edf6;overflow:hidden;}
.bar-track span {height:100%;display:block;background:#2864f0;}
@media(max-width:900px) {.admin-wrap{padding:0}.admin-hero{padding:24px 18px 75px}.st-key-hero_button{margin-left:18px !important;}}
/* MELHORIA DA LEGIBILIDADE — dentro da tag style */
.metric-card strong {font-size:28px !important;}
.metric-card small {font-size:13px !important;}
.metric-card em {font-size:14px !important;}
.section-title {font-size:19px !important;}
.section-hint {font-size:13px !important;}
.action-card {min-height:125px;}
.action-card h4 {font-size:15px !important;}
.action-card p {font-size:13px !important;line-height:1.5 !important;}
.st-key-actions button {font-size:12px !important;min-height:34px !important;}
.mini-panel h4 {font-size:15px !important;}
.mini-panel p, .reserve-line, .bar-label {font-size:12px !important;}
.reserve-line small {font-size:11px !important;}
</style>
""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sidebar-brand">▦ &nbsp; Reserva de Salas<small>SISTEMA ACADÊMICO</small></div>', unsafe_allow_html=True)
        itens = [
            ("⌂", "Início"),
            ("▦", "Salas"),
            ("⌖", "Mapa"),
            ("▣", "Reservas"),
            ("♙", "Usuários cadastrados"),
            ("⚙", "Administração"),
        ]
        if st.session_state.admin_pagina not in {pagina for _, pagina in itens}:
            st.session_state.admin_pagina = "Início"
        for icone, pagina in itens:
            if st.button(f"{icone}  {pagina}", key=f"side_{pagina}", use_container_width=True,
                         type="primary" if st.session_state.admin_pagina == pagina else "secondary"):
                navegar(pagina)
        st.markdown('<div class="sidebar-label">CONTA</div>', unsafe_allow_html=True)
        if st.button("↪  Sair", key="admin_sair", use_container_width=True):
            from utils.estado import fazer_logout
            fazer_logout()
            st.rerun()

    pagina = st.session_state.admin_pagina
    st.markdown(f'<div class="page-header">{escape(pagina)}<small>Sistema de Reserva de Salas · Campus Central</small></div>', unsafe_allow_html=True)
    
    
    
    
    if pagina == "Salas":
        from main import pagina_minhas_salas

        usuario = st.session_state.get("usuario")

        if usuario:
            pagina_minhas_salas(usuario)
        else:
            st.error("Usuário não encontrado. Faça login novamente.")

        return
    if pagina == "Reservas":
        from views.reserva_view import renderizar_reservas

        usuario = st.session_state.get("usuario")
        if usuario:
            renderizar_reservas(usuario, mostrar_titulo=False)
        else:
            st.error("Usuário não encontrado. Faça login novamente.")
        return
    if pagina == "Mapa":
        from views.mapa_campus_view import pagina_mapa_campus

        usuario = st.session_state.get("usuario")
        if usuario:
            pagina_mapa_campus(usuario)
        else:
            st.error("Usuário não encontrado. Faça login novamente.")
        return
    if pagina in {"Usuários cadastrados", "Administração"}:
        usuario = st.session_state.get("usuario")
        if not usuario:
            st.error("Faça login novamente.")
        elif pagina == "Usuários cadastrados":
            from views.admin_usuarios_firebase import renderizar_admin_usuarios

            renderizar_admin_usuarios(usuario)
        else:
            from views.admin_cadastro_figma import renderizar_cadastro_figma

            renderizar_cadastro_figma(usuario)
        return
    # HTML em uma string única: evita mostrar as tags como texto na tela.
    with st.container(key="admin_hero_wrap"):
        st.markdown(
            '<div class="admin-hero">'
            '<div class="eyebrow">PAINEL ADMINISTRATIVO</div>'
            '<h2>Bem-vindo ao Sistema de Reservas</h2>'
            '<p>Olá! Estamos prontos para ajudar você a começar.<br>'
            'Acesse as principais funções do sistema pelo menu ao lado.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="hero_button"):
            if st.button("Vamos começar", key="admin_comecar"):
                navegar("Administração")

    conteudo = st.container()
    with conteudo:
        usuario = st.session_state.get("usuario")
        reservas = []
        salas = []
        usuarios = []
        erros_carga = []

        try:
            from controllers.reserva_controller import listar_reservas_usuario
            reservas = listar_reservas_usuario(usuario)
        except Exception as erro:
            erros_carga.append(f"reservas: {erro}")

        try:
            from models.sala_firebase_model import listar_salas
            salas = listar_salas()
        except Exception as erro:
            erros_carga.append(f"salas: {erro}")

        try:
            from controllers.usuario_firebase_controller import listar_usuarios_admin
            usuarios = listar_usuarios_admin(usuario)
        except Exception as erro:
            erros_carga.append(f"usuários: {erro}")

        from models import reserva_firebase_model as reserva_model
        hoje = hoje_local().isoformat()
        pendentes = [
            reserva for reserva in reservas
            if reserva.get("status") == reserva_model.PENDENTE
        ]
        confirmadas_hoje = [
            reserva for reserva in reservas
            if reserva.get("status") == reserva_model.APROVADA
            and reserva.get("data") == hoje
        ]
        usuarios_ativos = [
            item for item in usuarios
            if item.get("status", "ativo") == "ativo"
        ]
        dados = [
            ("◷", str(len(pendentes)), "", "Reservas aguardando decisão"),
            ("▣", str(len(confirmadas_hoje)), "", "Reservas confirmadas hoje"),
            ("♙", str(len(usuarios_ativos)), "", "Usuários ativos"),
            ("▦", str(len(salas)), "", "Salas cadastradas"),
        ]
        if erros_carga:
            st.warning(
                "Alguns indicadores não puderam ser carregados. "
                "Confira a conexão com o Firebase e atualize a página."
            )
            return
        for inicio in range(0, len(dados), 2):
            metricas = st.columns(2, gap="small")
            for coluna, (icone, valor, sufixo, legenda) in zip(
                metricas,
                dados[inicio:inicio + 2],
            ):
                with coluna:
                    st.markdown(
                        f'<div class="metric-card"><span class="metric-icon">{icone}</span>'
                        f'<strong>{valor}<em>{sufixo}</em></strong><small>{legenda}</small></div>',
                        unsafe_allow_html=True,
                    )

        st.markdown('<div class="section-title">Ações rápidas</div><div class="section-hint">Escolha uma atividade para continuar no ambiente administrativo.</div>', unsafe_allow_html=True)
        esquerda, direita = st.columns([2.1, 1], gap="medium")
        with esquerda:
            acoes = [
                ("◷", "Analisar reservas", "Aprove, recuse ou cancele pedidos recebidos.", "Reservas"),
                ("＋", "Cadastrar usuário", "Crie uma conta e defina o perfil de acesso.", "Administração"),
                ("♙", "Consultar usuários", "Consulte e gerencie os usuários cadastrados.", "Usuários cadastrados"),
                ("▦", "Gerenciar salas", "Consulte as salas cadastradas no sistema.", "Salas"),
            ]
            with st.container(key="actions"):
                for i in range(0, len(acoes), 2):
                    cols = st.columns(2, gap="small")
                    for col, (icone, titulo, descricao, destino) in zip(cols, acoes[i:i + 2]):
                        with col:
                            st.markdown(
                                f'<div class="action-card"><span class="icon">{icone}</span>'
                                f'<h4>{escape(titulo)}</h4><p>{escape(descricao)}</p></div>',
                                unsafe_allow_html=True,
                            )
                            if st.button(titulo, key=f"acao_{titulo}", use_container_width=True):
                                navegar(destino)
        with direita:
            html_pendentes = '<div class="mini-panel"><h4>Fila de análise</h4>'
            if pendentes:
                for reserva in pendentes[:5]:
                    data_txt = reserva.get("data", "Data não informada")
                    try:
                        data_txt = datetime.strptime(
                            data_txt, "%Y-%m-%d"
                        ).strftime("%d/%m/%Y")
                    except (TypeError, ValueError):
                        pass
                    html_pendentes += (
                        '<div class="reserve-line">'
                        f'{escape(str(reserva.get("sala_nome", "Sala sem nome")))}'
                        '<small>'
                        f'{escape(data_txt)} · '
                        f'{escape(str(reserva.get("solicitante_nome", "Solicitante não informado")))}'
                        '</small></div>'
                    )
            else:
                html_pendentes += '<p>Não há pedidos aguardando decisão.</p>'
            st.markdown(html_pendentes + '</div>', unsafe_allow_html=True)
            if st.button("Abrir reservas", key="admin_abrir_reservas", use_container_width=True):
                navegar("Reservas")

            contagens_status = [
                ("Aprovadas", sum(r.get("status") == reserva_model.APROVADA for r in reservas)),
                ("Recusadas", sum(r.get("status") == reserva_model.RECUSADA for r in reservas)),
                ("Canceladas", sum(r.get("status") == reserva_model.CANCELADA for r in reservas)),
            ]
            html_status = '<div class="mini-panel"><h4>Resumo das reservas</h4>'
            for rotulo, quantidade in contagens_status:
                html_status += (
                    f'<div class="bar-label"><span>{rotulo}</span>'
                    f'<span>{quantidade}</span></div>'
                )
            st.markdown(html_status + '</div>', unsafe_allow_html=True)


