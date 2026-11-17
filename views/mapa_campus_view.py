
import os
import math

import streamlit as st
from PIL import Image, ImageDraw

from controllers.mapa_controller import (
    LOCAIS,
    CAMINHOS,
    LIGACOES,
    calcular_rota,
)


# Dimensoes originais utilizadas pelo controlador
LARGURA_BASE = 1535
ALTURA_BASE = 1024

LOCAIS_CAMPUS = list(LOCAIS.keys())


def converter_ponto(ponto, imagem):
    """Converte coordenadas para o tamanho atual da imagem."""
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


def desenhar_grafo_debug(imagem):
    """
    Mostra os corredores, conexoes e pontos do grafo.
    Nao altera o algoritmo de Dijkstra.
    """
    mapa = imagem.convert("RGB").copy()
    desenho = ImageDraw.Draw(mapa)

    escala = mapa.width / LARGURA_BASE

    largura_linha = max(2, int(4 * escala))
    raio = max(4, int(7 * escala))

    # Desenha todas as conexoes em verde
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

    # Desenha os pontos em amarelo
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

        # Identifica cada ponto
        desenho.text(
            (x + raio + 3, y - 12),
            nome,
            fill="#000000",
            stroke_width=2,
            stroke_fill="#FFFFFF",
        )

    return mapa


def desenhar_rota(imagem, rota):
    """Desenha a rota calculada pelo Dijkstra."""
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

    # Desenha a rota azul pontilhada
    for i in range(len(pontos) - 1):

        desenhar_linha_pontilhada(
            desenho,
            pontos[i],
            pontos[i + 1],
            cor="#0066FF",
            largura=largura,
        )

    # Marca a origem em azul
    x, y = pontos[0]

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

    # Marca o destino em vermelho
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

    return mapa


def pagina_mapa_campus(usuario):
    """Pagina do mapa do campus."""

    st.title("Mapa do Campus")

    st.write(
        "Encontre salas e outros espacos dentro do campus."
    )

    st.divider()

    # Selecao do destino
    st.subheader("Para onde deseja ir?")

    destino = st.selectbox(
        "Selecione seu destino",
        options=[""] + LOCAIS_CAMPUS,
        key="mapa_destino",
    )

    # Selecao da origem
    st.subheader("Ponto de partida")

    origem = st.selectbox(
        "Selecione onde voce esta",
        options=[""] + LOCAIS_CAMPUS,
        key="mapa_origem",
    )

    st.info(
        "A localizacao automatica pelo GPS sera adicionada "
        "em uma proxima etapa."
    )

    st.divider()

    st.subheader("Visualizacao do campus")

    # Modo desenvolvedor
    modo_debug = st.checkbox(
        "Mostrar corredores e pontos (Modo Desenvolvedor)",
        value=False,
        key="mapa_modo_debug",
    )

    if modo_debug:
        st.info(
            "Modo Desenvolvedor ativado. "
            "Linhas verdes representam conexoes, "
            "pontos amarelos representam os nos do grafo."
        )

    # Localizacao da imagem
    caminho_mapa = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "mapa_campus.png",
    )

    # Inicializa o armazenamento da rota
    if "rota_campus" not in st.session_state:
        st.session_state.rota_campus = None

    # Botao para calcular a rota
    if st.button(
        "Buscar destino",
        use_container_width=True,
    ):

        if not destino:
            st.warning(
                "Selecione o destino desejado."
            )
            st.session_state.rota_campus = None

        elif not origem:
            st.warning(
                "Selecione seu ponto de partida."
            )
            st.session_state.rota_campus = None

        elif origem == destino:
            st.warning(
                "O ponto de partida e o destino "
                "nao podem ser iguais."
            )
            st.session_state.rota_campus = None

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

                    st.success(
                        "Rota calculada com sucesso!"
                    )

                else:
                    st.session_state.rota_campus = None
                    st.error(
                        "Nao foi possivel calcular a rota."
                    )

            except (ValueError, KeyError) as erro:
                st.session_state.rota_campus = None
                st.error(
                    f"Erro ao calcular rota: {erro}"
                )

    # Verifica se a imagem existe
    if (
        os.path.isfile(caminho_mapa)
        and os.path.getsize(caminho_mapa) > 0
    ):

        try:
            with Image.open(caminho_mapa) as arquivo:
                imagem = arquivo.convert("RGB")

            # Primeiro desenha o grafo, quando ativado
            if modo_debug:
                imagem = desenhar_grafo_debug(
                    imagem
                )

            # Depois desenha a rota sobre o mapa
            dados_rota = st.session_state.rota_campus

            if dados_rota:
                imagem = desenhar_rota(
                    imagem,
                    dados_rota["pontos"],
                )

                st.write(
                    f"**Origem:** {dados_rota['origem']}  "
                    f"**Destino:** {dados_rota['destino']}"
                )

            # Exibe a imagem final
            st.image(
                imagem,
                caption="Mapa do Campus",
                use_container_width=True,
            )

        except (OSError, ValueError) as erro:
            st.error(
                "Nao foi possivel abrir a imagem do mapa. "
                "Verifique views/assets/mapa_campus.png."
            )
            st.caption(str(erro))

    else:
        st.warning(
            "Imagem nao encontrada ou vazia. "
            "Verifique se mapa_campus.png "
            "esta na pasta views/assets."
        )

    st.caption(
        "Rotas ilustrativas em desenvolvimento. "
        "Os trajetos ainda precisam ser conferidos "
        "com os caminhos reais do campus."
    )
