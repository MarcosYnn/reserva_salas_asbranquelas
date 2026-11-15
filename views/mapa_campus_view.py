
import os
import math
import streamlit as st
from PIL import Image, ImageDraw

from controllers.mapa_controller import LOCAIS, calcular_rota


LOCAIS_CAMPUS = list(LOCAIS.keys())


def desenhar_linha_pontilhada(desenho, inicio, fim, cor, largura=7):
    x1, y1 = inicio
    x2, y2 = fim

    distancia = math.hypot(x2 - x1, y2 - y1)

    if distancia == 0:
        return

    tamanho_traco = 12
    tamanho_espaco = 9
    passo = tamanho_traco + tamanho_espaco

    for posicao in range(0, int(distancia), passo):
        inicio_traco = posicao / distancia
        fim_traco = min(posicao + tamanho_traco, distancia) / distancia

        ponto1 = (
            x1 + (x2 - x1) * inicio_traco,
            y1 + (y2 - y1) * inicio_traco
        )

        ponto2 = (
            x1 + (x2 - x1) * fim_traco,
            y1 + (y2 - y1) * fim_traco
        )

        desenho.line([ponto1, ponto2], fill=cor, width=largura)


def desenhar_rota(imagem, rota):
    mapa = imagem.convert("RGB").copy()
    desenho = ImageDraw.Draw(mapa)

    # As coordenadas do controlador usam imagem de 1535 x 1024.
    escala_x = mapa.width / 1535
    escala_y = mapa.height / 1024

    pontos = [
        (int(x * escala_x), int(y * escala_y))
        for x, y in rota
    ]

    # Desenha a rota pontilhada
    for i in range(len(pontos) - 1):
        desenhar_linha_pontilhada(
            desenho,
            pontos[i],
            pontos[i + 1],
            cor="#0066FF",
            largura=max(3, int(7 * escala_x))
        )

    # Marca a origem com um ponto azul
    x, y = pontos[0]
    raio = max(7, int(13 * escala_x))

    desenho.ellipse(
        (x - raio, y - raio, x + raio, y + raio),
        fill="#0066FF",
        outline="white",
        width=3
    )

    # Marca o destino com um ponto vermelho
    x, y = pontos[-1]

    desenho.ellipse(
        (x - raio, y - raio, x + raio, y + raio),
        fill="#FF3333",
        outline="white",
        width=3
    )

    return mapa


def pagina_mapa_campus(usuario):

    st.title("Mapa do Campus")
    st.write("Encontre salas e outros espacos dentro do campus.")

    st.divider()

    st.subheader("Para onde deseja ir?")

    destino = st.selectbox(
        "Selecione seu destino",
        options=[""] + LOCAIS_CAMPUS
    )

    st.subheader("Ponto de partida")

    origem = st.selectbox(
        "Selecione onde voce esta",
        options=[""] + LOCAIS_CAMPUS
    )

    st.info(
        "A localizacao automatica pelo GPS sera adicionada "
        "em uma proxima etapa."
    )

    st.subheader("Visualizacao do campus")

    caminho_mapa = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "mapa_campus.png"
    )

    # Guarda a rota entre atualizacoes do Streamlit
    if "rota_campus" not in st.session_state:
        st.session_state.rota_campus = None

    if st.button("Buscar destino", use_container_width=True):

        if not destino:
            st.warning("Selecione o destino desejado.")
            st.session_state.rota_campus = None

        elif not origem:
            st.warning("Selecione seu ponto de partida.")
            st.session_state.rota_campus = None

        elif origem == destino:
            st.warning(
                "O ponto de partida e o destino nao podem ser iguais."
            )
            st.session_state.rota_campus = None

        else:
            rota = calcular_rota(origem, destino)

            if rota:
                st.session_state.rota_campus = {
                    "origem": origem,
                    "destino": destino,
                    "pontos": rota
                }

                st.success("Rota calculada com sucesso!")
            else:
                st.session_state.rota_campus = None
                st.error("Nao foi possivel calcular a rota.")

    # Carrega a imagem e desenha a rota
    if os.path.isfile(caminho_mapa) and os.path.getsize(caminho_mapa) > 0:

        try:
            with Image.open(caminho_mapa) as arquivo:
                imagem = arquivo.convert("RGB")

            dados_rota = st.session_state.rota_campus

            if dados_rota:
                imagem = desenhar_rota(
                    imagem,
                    dados_rota["pontos"]
                )

                st.write(
                    f"**Origem:** {dados_rota['origem']}  "
                    f"**Destino:** {dados_rota['destino']}"
                )

            st.image(
                imagem,
                caption="Mapa do Campus",
                use_container_width=True
            )

        except (OSError, ValueError):
            st.error(
                "Nao foi possivel abrir a imagem do mapa. "
                "Verifique o arquivo views/assets/mapa_campus.png."
            )

    else:
        st.warning(
            "Imagem nao encontrada ou vazia. "
            "Verifique se mapa_campus.png esta na pasta views/assets."
        )

    st.caption(
        "Rotas ilustrativas em desenvolvimento. "
        "Os trajetos ainda precisam ser conferidos com os "
        "caminhos reais do campus."
    )
