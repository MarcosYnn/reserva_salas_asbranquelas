
import os
import math
import time

import streamlit as st
from PIL import Image, ImageDraw

from controllers.mapa_controller import (
    LOCAIS,
    CAMINHOS,
    LIGACOES,
    calcular_rota,
    gerar_movimentacao,
)


LARGURA_BASE = 1535
ALTURA_BASE = 1024

LOCAIS_CAMPUS = list(LOCAIS.keys())


def converter_ponto(ponto, imagem):

    escala_x = imagem.width / LARGURA_BASE
    escala_y = imagem.height / ALTURA_BASE

    return (
        int(ponto[0] * escala_x),
        int(ponto[1] * escala_y),
    )


def desenhar_linha_pontilhada(
    desenho, inicio, fim, cor="#0066FF", largura=7
):

    x1, y1 = inicio
    x2, y2 = fim

    distancia = math.hypot(x2 - x1, y2 - y1)

    if distancia == 0:
        return

    tamanho_traco = 12
    tamanho_espaco = 9
    passo = tamanho_traco + tamanho_espaco

    for posicao in range(0, int(distancia) + 1, passo):

        inicio_traco = posicao / distancia

        fim_traco = min(
            posicao + tamanho_traco, distancia
        ) / distancia

        ponto1 = (
            int(x1 + (x2 - x1) * inicio_traco),
            int(y1 + (y2 - y1) * inicio_traco),
        )

        ponto2 = (
            int(x1 + (x2 - x1) * fim_traco),
            int(y1 + (y2 - y1) * fim_traco),
        )

        desenho.line(
            [ponto1, ponto2],
            fill=cor,
            width=largura,
        )


# ==========================================
# MODO DESENVOLVEDOR
# ==========================================

def desenhar_grafo_debug(imagem):

    mapa = imagem.convert("RGB").copy()
    desenho = ImageDraw.Draw(mapa)

    escala = mapa.width / LARGURA_BASE

    largura_linha = max(2, int(4 * escala))
    raio = max(4, int(7 * escala))

    for origem, destino in LIGACOES:

        if origem not in CAMINHOS or destino not in CAMINHOS:
            continue

        ponto1 = converter_ponto(
            CAMINHOS[origem], mapa
        )

        ponto2 = converter_ponto(
            CAMINHOS[destino], mapa
        )

        desenho.line(
            [ponto1, ponto2],
            fill="#00CC44",
            width=largura_linha,
        )

    for nome, coordenada in CAMINHOS.items():

        x, y = converter_ponto(coordenada, mapa)

        desenho.ellipse(
            (
                x - raio,
                y - raio,
                x + raio,
                y + raio,
            ),
            fill="#FFFF00",
            outline="#000000",
            width=2,
        )

        desenho.text(
            (x + raio + 3, y - 12),
            nome,
            fill="#000000",
            stroke_width=2,
            stroke_fill="#FFFFFF",
        )

    return mapa


# ==========================================
# DESENHO DAS ROTAS
# ==========================================

def desenhar_rota(imagem, rota, posicao_atual=None):

    mapa = imagem.convert("RGB").copy()
    desenho = ImageDraw.Draw(mapa)

    if not rota:
        return mapa

    pontos = [
        converter_ponto(ponto, mapa)
        for ponto in rota
    ]

    escala = mapa.width / LARGURA_BASE
    largura = max(3, int(7 * escala))
    raio = max(7, int(13 * escala))

    # Rota azul pontilhada

    for i in range(len(pontos) - 1):

        desenhar_linha_pontilhada(
            desenho,
            pontos[i],
            pontos[i + 1],
            cor="#0066FF",
            largura=largura,
        )

    # Posicao atual do usuario

    if posicao_atual is None:
        posicao_atual = rota[0]

    x, y = converter_ponto(
        posicao_atual, mapa
    )

    # Circulo externo da localizacao

    raio_externo = raio + 7

    desenho.ellipse(
        (
            x - raio_externo,
            y - raio_externo,
            x + raio_externo,
            y + raio_externo,
        ),
        outline="#80BFFF",
        width=3,
    )

    # Ponto azul em movimento

    desenho.ellipse(
        (
            x - raio,
            y - raio,
            x + raio,
            y + raio,
        ),
        fill="#0066FF",
        outline="#FFFFFF",
        width=3,
    )

    # Destino vermelho

    x, y = pontos[-1]

    desenho.ellipse(
        (
            x - raio,
            y - raio,
            x + raio,
            y + raio,
        ),
        fill="#FF3333",
        outline="#FFFFFF",
        width=3,
    )

    # Mostra a chegada ao destino

    if posicao_atual == rota[-1]:

        raio_chegada = raio + 4

        desenho.ellipse(
            (
                x - raio_chegada,
                y - raio_chegada,
                x + raio_chegada,
                y + raio_chegada,
            ),
            outline="#00CC44",
            width=4,
        )

    return mapa


# ==========================================
# PAGINA DO MAPA
# ==========================================

def pagina_mapa_campus(usuario):
    from controllers.autorizacao_controller import exigir_tipo

    exigir_tipo(usuario, ["Locatário", "Proprietário", "Administrador"])


    st.markdown(
        """
        <style>
        .app-page-header {
            background: #ffffff;
            border-bottom: 1px solid #e1e8f3;
            padding: 15px 24px;
            margin: 0 -1.5rem 0;
            color: #101c36;
        }
        .app-page-header h2 {
            font-size: 15px;
            font-weight: 750;
        }
        .app-page-header p {
            margin-top: 4px;
            font-size: 10px;
        }
        [data-testid="stImage"] {
            max-width: 1050px;
            margin-left: auto;
            margin-right: auto;
            display: flex;
            justify-content: center;
        }
        [data-testid="stImage"] img {
            max-width: 100%;
            width: auto;
            height: auto;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Mapa do Campus")

    st.write(
        "Encontre salas e outros espacos dentro do campus."
    )

    st.divider()

    col_origem, col_destino = st.columns(2, gap="large")

    with col_origem:
        origem = st.selectbox(
            "Ponto de partida",
            options=[""] + LOCAIS_CAMPUS,
            key="mapa_origem",
        )

    with col_destino:
        destino = st.selectbox(
            "Destino",
            options=[""] + LOCAIS_CAMPUS,
            key="mapa_destino",
        )

    st.info(
        "A navegacao utiliza movimentacao simulada. "
        "O GPS real sera integrado futuramente."
    )

    st.divider()

    st.subheader("Visualizacao do campus")

    eh_admin = (
        isinstance(usuario, dict)
        and usuario.get("tipo") == "Administrador"
    )

    if eh_admin:
        modo_debug = st.checkbox(
            "Mostrar corredores e pontos (Modo Desenvolvedor)",
            value=False,
            key="mapa_modo_debug",
        )
    else:
        modo_debug = False

    if modo_debug:

        st.info(
            "Modo Desenvolvedor ativado. "
            "Linhas verdes representam conexoes, "
            "pontos amarelos representam os nos do grafo."
        )

    caminho_mapa = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "mapa_campus.png",
    )

    # Estados da navegacao

    if "rota_campus" not in st.session_state:
        st.session_state.rota_campus = None

    if "posicao_campus" not in st.session_state:
        st.session_state.posicao_campus = None

    if "chegada_campus" not in st.session_state:
        st.session_state.chegada_campus = False

    # Limpa a rota ao mudar origem ou destino

    dados_anteriores = st.session_state.rota_campus

    if dados_anteriores and (
        dados_anteriores["origem"] != origem
        or dados_anteriores["destino"] != destino
    ):

        st.session_state.rota_campus = None
        st.session_state.posicao_campus = None
        st.session_state.chegada_campus = False

    # Botao para calcular a rota

    col_vazia_esq, col_busca, col_vazia_dir = st.columns([1, 2, 1])
    with col_busca:
        buscar_destino = st.button(
            "Buscar destino",
            use_container_width=True,
        )

    if buscar_destino:

        st.session_state.rota_campus = None
        st.session_state.posicao_campus = None
        st.session_state.chegada_campus = False

        if not destino:

            st.warning(
                "Selecione o destino desejado."
            )

        elif not origem:

            st.warning(
                "Selecione seu ponto de partida."
            )

        elif origem == destino:

            st.warning(
                "Voce ja esta no destino selecionado."
            )

        else:

            try:

                rota = calcular_rota(
                    origem, destino
                )

                if rota:

                    st.session_state.rota_campus = {
                        "origem": origem,
                        "destino": destino,
                        "pontos": rota,
                    }

                    st.session_state.posicao_campus = rota[0]

                    st.success(
                        "Rota calculada com sucesso!"
                    )

                else:

                    st.error(
                        "Nao foi possivel calcular a rota."
                    )

            except (ValueError, KeyError) as erro:

                st.error(
                    f"Erro ao calcular rota: {erro}"
                )

    # Verifica a imagem

    if (
        os.path.isfile(caminho_mapa)
        and os.path.getsize(caminho_mapa) > 0
    ):

        try:

            with Image.open(caminho_mapa) as arquivo:
                imagem = arquivo.convert("RGB")

            if modo_debug:

                imagem = desenhar_grafo_debug(
                    imagem
                )

            _, coluna_mapa, _ = st.columns([1, 4, 1])
            dados_rota = st.session_state.rota_campus

            if dados_rota:

                rota = dados_rota["pontos"]

                st.write(
                    f"**Origem:** {dados_rota['origem']}  "
                    f"**Destino:** {dados_rota['destino']}"
                )

                # ==========================================
                # CONTROLES DE MOVIMENTACAO
                # ==========================================

                col1, col2 = st.columns(2)

                with col1:

                    iniciar = st.button(
                        "Simular navegacao",
                        use_container_width=True,
                    )

                with col2:

                    reiniciar = st.button(
                        "Reiniciar navegacao",
                        use_container_width=True,
                    )

                if reiniciar or iniciar:

                    st.session_state.posicao_campus = rota[0]

                    st.session_state.chegada_campus = False

                espaco_mapa = coluna_mapa.empty()
                espaco_status = st.empty()

                progresso = st.progress(
                    100 if st.session_state.chegada_campus else 0
                )

                espaco_mapa.image(
                    desenhar_rota(
                        imagem,
                        rota,
                        st.session_state.posicao_campus,
                    ),
                    caption="Mapa do Campus",
                    use_container_width=True,
                )

                if iniciar:

                    posicoes = gerar_movimentacao(
                        rota,
                        passo=8
                    )

                    if posicoes:

                        espaco_status.info(
                            "Navegacao simulada em andamento..."
                        )

                        total = max(
                            1, len(posicoes) - 1
                        )

                        # Movimenta o ponto azul

                        for i, posicao in enumerate(posicoes):

                            st.session_state.posicao_campus = posicao

                            mapa_atual = desenhar_rota(
                                imagem,
                                rota,
                                posicao,
                            )

                            espaco_mapa.image(
                                mapa_atual,
                                caption="Mapa do Campus",
                                use_container_width=True,
                            )

                            percentual = int(
                                i / total * 100
                            )

                            progresso.progress(percentual)

                            time.sleep(0.05)

                        st.session_state.posicao_campus = rota[-1]

                        st.session_state.chegada_campus = True

                        progresso.progress(100)

                        espaco_status.success(
                            f"Simulacao concluida! "
                            f"Destino: {dados_rota['destino']}"
                        )

                elif st.session_state.chegada_campus:

                    espaco_status.success(
                        f"Simulacao concluida! "
                        f"Destino: {dados_rota['destino']}"
                    )

            else:

                with coluna_mapa:
                    st.image(
                        imagem,
                        caption="Mapa do Campus",
                        use_container_width=True,
                    )

        except (OSError, ValueError) as erro:

            st.error(
                "Nao foi possivel abrir ou desenhar o mapa."
            )

            st.caption(str(erro))

    else:

        st.warning(
            "Imagem nao encontrada ou vazia. "
            "Verifique views/assets/mapa_campus.png."
        )

    st.caption(
        "Navegacao ilustrativa e simulada. "
        "Os trajetos ainda precisam ser conferidos "
        "com os caminhos reais do campus."
    )

