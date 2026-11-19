from datetime import date, datetime, time
from views.admin_view import mostrar_admin

import streamlit as st

from controllers.sala_controller import (
    atualizar_sala,
    excluir_sala,
)

from controllers.reserva_controller import (
    buscar_conflitos,
    listar_reservas_ativas_para_busca,
    listar_reservas_usuario,
)

from controllers.autorizacao_controller import exigir_tipo
from controllers.reserva_controller import (
    listar_reservas_ativas_para_busca,
    listar_reservas_usuario,
)
from utils.componentes import (
    render_card,
    renderizar_banner_dashboard,
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

from views.calendario_locatario_view import renderizar_calendario_locatario
from views.reserva_view import renderizar_reservas


def _formatar_data(data_iso):
    try:
        return date.fromisoformat(data_iso).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return data_iso or "—"


def _renderizar_acoes_rapidas(acoes, chave_prefixo, painel=None):
    st.markdown(f"""
    <style>
    .dashboard-hero {{box-sizing:border-box;min-height:215px;padding:1.65rem 1.8rem 4rem;}}
    .card {{box-sizing:border-box;padding:13px !important;min-height:103px !important;border-radius:11px !important;box-shadow:none !important;}}
    .profile-action-card {{background:#fff;border:1px solid #dce5f1;border-radius:11px;padding:12px;min-height:125px;}}
    .profile-action-card .icon {{display:inline-block;border-radius:8px;padding:5px 8px;background:#eff4fb;color:#3776f5;font-size:15px;}}
    .profile-action-card h4 {{font-size:15px;color:#132d54;margin:7px 0 3px;}}
    .profile-action-card p {{font-size:13px;color:#7589a7;line-height:1.5;margin:0;}}
    .st-key-{chave_prefixo}_grid [data-testid="stButton"] button {{font-size:12px !important;min-height:34px !important;margin-top:-3px !important;}}
    .st-key-{chave_prefixo}_panel {{background:#fff;border:1px solid #dce5f1;border-radius:11px;padding:13px;}}
    </style>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-section-title">Ações rápidas</div>'
        '<div class="dashboard-section-caption">'
        "Acesse diretamente as funções mais usadas da sua conta."
        "</div>",
        unsafe_allow_html=True,
    )

    coluna_acoes, coluna_painel = st.columns(
        [2.1, 1] if painel else [1],
        gap="medium",
    )
    with coluna_acoes:
        with st.container(key=f"{chave_prefixo}_grid"):
            for inicio in range(0, len(acoes), 2):
                colunas = st.columns(2, gap="small")
                for coluna, (icone, titulo, descricao, destino) in zip(
                    colunas,
                    acoes[inicio:inicio + 2],
                ):
                    with coluna:
                        st.markdown(
                            '<div class="profile-action-card">'
                            f'<span class="icon">{icone}</span>'
                            f'<h4>{titulo}</h4><p>{descricao}</p></div>',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            titulo,
                            key=f"{chave_prefixo}_{titulo}",
                            use_container_width=True,
                        ):
                            if destino == "__nova_sala__":
                                st.session_state.pagina_atual = "Dashboard"
                                st.session_state.abrir_form_nova_sala = True
                            else:
                                st.session_state.pagina_atual = destino
                            st.rerun()

    if painel:
        with coluna_painel:
            with st.container(key=f"{chave_prefixo}_panel"):
                painel()


def _renderizar_resumo_reservas(reservas):
    status_reservas = [
        ("Aprovadas", "Aprovada"),
        ("Pendentes", "Pendente"),
        ("Recusadas", "Recusada"),
        ("Canceladas", "Cancelada"),
    ]

    st.markdown("#### Resumo das reservas")
    for rotulo, status in status_reservas:
        total = sum(
            reserva.get("status") == status
            for reserva in reservas
        )
        coluna_rotulo, coluna_total = st.columns([3, 1])
        coluna_rotulo.caption(rotulo)
        coluna_total.markdown(f"**{total}**")


def _renderizar_salas_mais_usadas(reservas, salas):
    nomes_salas = {
        str(sala.get("id")): sala.get("nome", "Sala sem nome")
        for sala in salas
    }
    usos = {}
    for reserva in reservas:
        if reserva.get("status") != "Aprovada":
            continue
        sala_id = str(reserva.get("sala_id") or "")
        nome = nomes_salas.get(
            sala_id,
            reserva.get("sala_nome", "Sala sem nome"),
        )
        usos[nome] = usos.get(nome, 0) + 1

    mais_usadas = sorted(
        usos.items(),
        key=lambda item: (-item[1], item[0].casefold()),
    )[:5]

    st.markdown("#### Salas mais usadas")
    st.caption("Com base nas reservas aprovadas das suas salas.")
    if not mais_usadas:
        st.info("Ainda não há reservas aprovadas para suas salas.")
        return

    maior_uso = mais_usadas[0][1]
    for nome, total in mais_usadas:
        st.markdown(f"**{nome}** · {total} reserva(s)")
        st.progress(total / maior_uso)


# ==========================================
# PÁGINAS — LOCATÁRIO
# ==========================================

def pagina_dashboard_locatario(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    renderizar_banner_dashboard(
        "Área do locatário",
        usuario["nome"].split()[0],
        "Encontre uma sala para o seu próximo compromisso.",
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
    pendentes = [
        reserva
        for reserva in minhas_reservas
        if reserva.get("status") == "Pendente"
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

    indicadores = [
        ("📅 Reservas hoje", len(reservas_hoje), f"{len(aprovadas_hoje)} aprovada(s)"),
        ("⏳ Pedidos pendentes", len(pendentes), "Aguardando retorno"),
        ("📋 Minhas reservas", len(minhas_reservas), "Total de pedidos"),
        (
            "⏰ Próxima reserva",
            proxima.get("hora_inicio", "—") if proxima else "—",
            proxima.get("sala_nome", "Sala") if proxima else "Nenhuma agendada",
        ),
    ]
    for inicio in range(0, len(indicadores), 2):
        colunas_indicadores = st.columns(2, gap="small")
        for coluna, (titulo, valor, detalhe) in zip(
            colunas_indicadores,
            indicadores[inicio:inicio + 2],
        ):
            with coluna:
                render_card(titulo, valor, detalhe)

    _renderizar_acoes_rapidas(
        [
            ("🔎", "Buscar salas", "Encontre uma sala para sua próxima reserva.", "Buscar Salas"),
            ("📋", "Minhas reservas", "Consulte ou cancele seus pedidos.", "Minhas Reservas"),
            ("🗓️", "Calendário", "Veja as reservas confirmadas no calendário.", "Calendário"),
            ("♡", "Favoritos", "Acesse as salas que você salvou.", "Favoritos"),
        ],
        "acoes_locatario",
        painel=lambda: _renderizar_resumo_reservas(minhas_reservas),
    )


def pagina_buscar_salas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="page-intro">'
        "Filtre por data, horário e capacidade."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="search-section-heading">'
        "🔎 Encontre uma sala disponível</div>",
        unsafe_allow_html=True,
    )

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

    col5, col6 = st.columns(2)

    with col5:
        necessita_equipamentos = st.checkbox(
            "Precisa de equipamentos especiais"
        )

    with col6:
        evento_institucional = st.checkbox(
            "É um evento institucional"
        )

    if st.button("🔎 Procurar salas", type="primary"):
        if horario_fim <= horario_inicio:
            st.session_state.resultado_busca = []
            st.session_state.busca_conflitos_por_sala = {}
            st.error("O horário final deve ser depois do horário inicial.")
        else:
            data_iso = data_busca.strftime("%Y-%m-%d")
            inicio_txt = horario_inicio.strftime("%H:%M")
            fim_txt = horario_fim.strftime("%H:%M")

            st.session_state.busca_data_iso = data_iso
            st.session_state.busca_hora_inicio = inicio_txt
            st.session_state.busca_hora_fim = fim_txt
            st.session_state.busca_necessita_equipamentos = (
                necessita_equipamentos
            )
            st.session_state.busca_evento_institucional = (
                evento_institucional
            )

            try:
                reservas_ativas = listar_reservas_ativas_para_busca(usuario)
            except Exception as erro:
                st.error(f"Não foi possível consultar reservas: {erro}")
                reservas_ativas = []

            salas_encontradas = [
                sala
                for sala in st.session_state.get("salas", [])
                if sala["capacidade"] >= pessoas
            ]

            conflitos_por_sala = {}

            for sala in salas_encontradas:
                conflitos = buscar_conflitos(
                    reservas=reservas_ativas,
                    sala_id=sala["id"],
                    data=data_iso,
                    hora_inicio=inicio_txt,
                    hora_fim=fim_txt,
                )

                if conflitos:
                    conflitos_por_sala[str(sala["id"])] = conflitos

            st.session_state.resultado_busca = salas_encontradas
            st.session_state.busca_conflitos_por_sala = conflitos_por_sala

    resultado = st.session_state.get("resultado_busca")

    if resultado is not None:
        if resultado:
            conflitos_por_sala = st.session_state.get(
                "busca_conflitos_por_sala",
                {},
            )

            if conflitos_por_sala:
                st.warning(
                    "Algumas salas têm pedidos que se sobrepõem a esse "
                    "horário. Você ainda pode enviar o pedido; ele será "
                    "sinalizado para análise do administrador."
                )

            st.success(
                f"Encontramos {len(resultado)} sala(s) "
                "com a capacidade selecionada."
            )
            colunas = st.columns(3)

            for indice, sala in enumerate(resultado):
                if str(sala["id"]) in conflitos_por_sala:
                    st.warning(
                        f"A sala {sala['nome']} tem conflito de horário. "
                        "O administrador precisará analisar o pedido."
                    )

                render_sala_card(
                    sala=sala,
                    coluna=colunas[indice % 3],
                    contexto="busca",
                    usuario_atual=usuario,
                )
        else:
            st.warning(
                "Nenhuma sala atende à capacidade selecionada."
            )


def pagina_minhas_reservas(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="page-intro">'
        "Consulte a situação dos seus pedidos e os horários reservados."
        "</div>",
        unsafe_allow_html=True,
    )
    renderizar_reservas(usuario, mostrar_titulo=False)


def pagina_favoritos(usuario):
    exigir_tipo(usuario, [TIPO_LOCATARIO])

    st.markdown(
        '<div class="page-intro">'
        "Consulte as salas que você marcou para encontrar mais facilmente."
        "</div>",
        unsafe_allow_html=True,
    )

    favoritos_ids = st.session_state.get("favoritos", set())

    favoritas = [
        sala
        for sala in st.session_state.get("salas", [])
        if sala.get("id") in favoritos_ids
    ]

    if not favoritas:
        st.markdown(
            '<div class="dashboard-section-title">'
            "Você ainda não tem salas favoritas</div>"
            '<div class="dashboard-section-caption">'
            "Explore as salas disponíveis e use o coração para salvá-las aqui."
            "</div>",
            unsafe_allow_html=True,
        )
        st.info("Sua lista de favoritos está vazia.")

        if st.button(
            "Buscar salas",
            type="primary",
            key="ir_buscar_salas_favoritos",
        ):
            st.session_state.pagina_atual = "Buscar Salas"
            st.rerun()

        return

    st.markdown(
        '<div class="dashboard-section-title">Salas favoritas</div>'
        '<div class="dashboard-section-caption">'
        f"Você salvou {len(favoritas)} sala(s). "
        "Use o coração para remover uma sala dos favoritos."
        "</div>",
        unsafe_allow_html=True,
    )

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

    email_ou_login = usuario.get("email") or usuario.get("login")

    try:
        total_reservas = len(listar_reservas_usuario(usuario))
    except Exception:
        total_reservas = 0

    total_favoritos = len(
        st.session_state.get("favoritos", set())
    )

    st.markdown(
        '<div class="page-intro">'
        "Confira os dados da sua conta e sua atividade no sistema."
        "</div>",
        unsafe_allow_html=True,
    )

    coluna_dados, coluna_atividade = st.columns([2, 1])

    with coluna_dados:
        with st.container(border=True):
            st.markdown("### 👤 Dados da conta")
            st.write(f"**Nome:** {usuario.get('nome', 'Não informado')}")
            st.write(
                f"**Tipo de conta:** "
                f"{usuario.get('tipo', 'Não informado')}"
            )

            if email_ou_login:
                st.write(f"**E-mail / usuário:** {email_ou_login}")

    with coluna_atividade:
        with st.container(border=True):
            st.markdown("### 📊 Minha atividade")
            st.metric("Reservas", total_reservas)
            st.metric("Salas favoritas", total_favoritos)


# ==========================================
# PÁGINAS — PROPRIETÁRIO
# ==========================================

def pagina_dashboard_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    rotulo_dashboard = (
        "Painel administrativo"
        if usuario.get("tipo") == TIPO_ADMIN
        else "Área do proprietário"
    )
    renderizar_banner_dashboard(
        rotulo_dashboard,
        usuario["nome"].split()[0],
        "Acompanhe suas salas e os pedidos recebidos.",
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

    indicadores = [
        ("Salas cadastradas", len(minhas_salas), "Nas suas salas"),
        ("Pedidos recebidos", len(reservas_recebidas), "Total"),
        (
            "Pedidos pendentes",
            len(pendentes),
            "Aguardando decisão do administrador",
        ),
        ("Reservas aprovadas", len(aprovadas), "Pedidos confirmados"),
    ]
    for inicio in range(0, len(indicadores), 2):
        colunas_indicadores = st.columns(2, gap="small")
        for coluna, (titulo, valor, detalhe) in zip(
            colunas_indicadores,
            indicadores[inicio:inicio + 2],
        ):
            with coluna:
                render_card(titulo, valor, detalhe)

    _renderizar_acoes_rapidas(
        [
            ("▦", "Gerenciar salas", "Edite os dados das salas vinculadas à sua conta.", "Minhas Salas"),
            ("◷", "Consultar pedidos", "Acompanhe as solicitações recebidas para suas salas.", "Pedidos de Reserva"),
            ("＋", "Cadastrar sala", "Adicione uma nova sala ao sistema.", "__nova_sala__"),
            ("◉", "Meu perfil", "Consulte os dados da sua conta.", "Perfil"),
        ],
        "acoes_proprietario",
        painel=lambda: _renderizar_salas_mais_usadas(
            reservas_recebidas,
            minhas_salas,
        ),
    )

    st.markdown(
        '<div class="dashboard-section-title">'
        "Pedidos para minhas salas</div>"
        '<div class="dashboard-section-caption">'
        "Consulte a situação das reservas das suas salas.</div>",
        unsafe_allow_html=True,
    )
    renderizar_reservas(usuario, mostrar_titulo=False)

    st.markdown("---")

    with st.expander(
        "Cadastrar nova sala",
        expanded=st.session_state.pop("abrir_form_nova_sala", False),
    ):
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
        '<div class="page-intro">'
        "Consulte e gerencie as salas vinculadas à sua conta."
        "</div>",
        unsafe_allow_html=True,
    )

    minhas_salas = salas_de(usuario["login"])

    st.markdown(
        '<div class="dashboard-section-title">Salas cadastradas</div>'
        '<div class="dashboard-section-caption">'
        f"{len(minhas_salas)} sala(s) vinculada(s) à sua conta."
        "</div>",
        unsafe_allow_html=True,
    )

    if not minhas_salas:
        st.info("Você ainda não cadastrou nenhuma sala.")
        st.caption("O cadastro de uma sala está disponível na página Início.")
        return

    colunas = st.columns(3)

    for indice, sala in enumerate(minhas_salas):
        sala_id = sala["id"]

        with colunas[indice % 3]:
            with st.container(border=True):
                st.markdown(f"### 🏢 {sala.get('nome', 'Sala')}")
                st.caption(
                    f"👥 Capacidade: {sala.get('capacidade', '—')} pessoas"
                )
                st.write(f"🖥️ Recursos: {sala.get('recursos') or 'Nenhum'}")
                st.write(f"📍 Localização: {sala.get('andar') or '—'}")

                with st.expander("Editar ou excluir sala"):
                    with st.form(f"form_editar_sala_{sala_id}"):
                        col_nome, col_localizacao = st.columns(2)

                        with col_nome:
                            nome = st.text_input(
                                "Nome da sala",
                                value=sala.get("nome", ""),
                                key=f"nome_sala_{sala_id}",
                            )
                            capacidade = st.number_input(
                                "Capacidade",
                                min_value=1,
                                value=max(
                                    1,
                                    int(sala.get("capacidade") or 1),
                                ),
                                key=f"capacidade_sala_{sala_id}",
                            )

                        with col_localizacao:
                            localizacao = st.text_input(
                                "Localização",
                                value=sala.get("andar", ""),
                                key=f"localizacao_sala_{sala_id}",
                            )

                        st.caption("Recursos disponíveis")

                        opcoes_recursos = [
                            ("projetor", "Projetor"),
                            ("computador", "Computador"),
                            ("internet", "Wi-Fi"),
                            ("webcam", "Webcam"),
                            ("quadro", "Quadro branco"),
                            ("ar_condicionado", "Ar-condicionado"),
                        ]

                        colunas_recursos = st.columns(2)
                        recursos_selecionados = {}

                        for posicao, (chave, rotulo) in enumerate(
                            opcoes_recursos
                        ):
                            with colunas_recursos[posicao % 2]:
                                recursos_selecionados[chave] = st.checkbox(
                                    rotulo,
                                    value=bool(sala.get(chave, False)),
                                    key=f"{chave}_sala_{sala_id}",
                                )

                        salvar = st.form_submit_button(
                            "Salvar alterações",
                            type="primary",
                            use_container_width=True,
                        )

                    if salvar:
                        recursos_marcados = [
                            chave
                            for chave, marcado
                            in recursos_selecionados.items()
                            if marcado
                        ]

                        try:
                            atualizar_sala(
                                usuario=usuario,
                                sala_id=sala_id,
                                nome=nome,
                                capacidade=capacidade,
                                localizacao=localizacao,
                                recursos_marcados=recursos_marcados,
                            )
                            st.success("Sala atualizada.")
                            st.rerun()
                        except Exception as erro:
                            st.error(
                                f"Não foi possível atualizar a sala: {erro}"
                            )

                    st.divider()

                    confirmar_exclusao = st.checkbox(
                        "Confirmo que quero excluir esta sala.",
                        key=f"confirmar_exclusao_sala_{sala_id}",
                    )

                    if st.button(
                        "Excluir sala",
                        key=f"excluir_sala_{sala_id}",
                        disabled=not confirmar_exclusao,
                        use_container_width=True,
                    ):
                        try:
                            excluir_sala(
                                usuario=usuario,
                                sala_id=sala_id,
                            )
                            st.success("Sala excluída.")
                            st.rerun()
                        except Exception as erro:
                            st.error(
                                f"Não foi possível excluir a sala: {erro}"
                            )


def pagina_pedidos_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    st.markdown(
        '<div class="page-intro">'
        "Acompanhe os pedidos recebidos para as suas salas."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dashboard-section-title">Pedidos recebidos</div>'
        '<div class="dashboard-section-caption">'
        "Expanda um pedido para consultar os detalhes e o status."
        "</div>",
        unsafe_allow_html=True,
    )

    renderizar_reservas(usuario, mostrar_titulo=False)


def pagina_perfil_proprietario(usuario):
    exigir_tipo(usuario, [TIPO_PROPRIETARIO, TIPO_ADMIN])

    salas_usuario = salas_de(usuario.get("login"))
    email_ou_login = usuario.get("email") or usuario.get("login")

    st.markdown(
        '<div class="page-intro">'
        "Confira os dados da sua conta e as salas vinculadas a ela."
        "</div>",
        unsafe_allow_html=True,
    )

    coluna_dados, coluna_resumo = st.columns([2, 1])

    with coluna_dados:
        with st.container(border=True):
            st.markdown("### 👤 Dados da conta")
            st.write(f"**Nome:** {usuario.get('nome', 'Não informado')}")
            st.write(
                f"**Tipo de conta:** "
                f"{usuario.get('tipo', 'Não informado')}"
            )

            if email_ou_login:
                st.write(f"**E-mail / usuário:** {email_ou_login}")

    with coluna_resumo:
        with st.container(border=True):
            st.markdown("### 🏢 Suas salas")
            st.metric("Salas cadastradas", len(salas_usuario))
            st.caption("Salas vinculadas à sua conta.")


# ==========================================
# PÁGINAS — ADMINISTRADOR
# ==========================================

def pagina_admin(usuario):
    exigir_tipo(usuario, [TIPO_ADMIN])
    mostrar_admin()


# ==========================================
# MENUS POR PERFIL
# ==========================================

PAGINAS_LOCATARIO = {
    "Dashboard": pagina_dashboard_locatario,
    "Buscar Salas": pagina_buscar_salas,
    "Minhas Reservas": pagina_minhas_reservas,
    "Calendário": renderizar_calendario_locatario,
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
