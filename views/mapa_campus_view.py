
import os
import streamlit as st


LOCAIS_CAMPUS = [
    "Entrada Principal",
    "Recepcao e Informacoes",
    "Laboratorio de Informatica 1",
    "Laboratorio de Informatica 2",
    "Laboratorio de Informatica 3",
    "Laboratorio de Informatica 4",
    "Laboratorio de Informatica 5",
    "Laboratorio de Informatica 6",
    "Salas de Aula - Bloco A",
    "Salas de Aula - Bloco B",
    "Salas de Aula - Bloco C",
    "Biblioteca",
    "Auditorio",
    "Anfiteatro 1",
    "Anfiteatro 2",
    "Espaco Maker",
    "Praca Central",
    "Cantina",
    "Piscina",
    "Quadra Poliesportiva 1",
    "Quadra Poliesportiva 2",
    "Laboratorio de Engenharia Civil",
    "Laboratorio de Fisioterapia",
    "Laboratorio de Odontologia",
    "Laboratorio de Medicina",
]


def pagina_mapa_campus(usuario):

    st.title("Mapa do Campus")
    st.write("Encontre salas e outros espacos dentro do campus.")

    st.divider()

    # Escolha do destino
    st.subheader("Para onde deseja ir?")

    destino = st.selectbox(
        "Selecione seu destino",
        options=[""] + LOCAIS_CAMPUS
    )

    # Ponto de partida
    st.subheader("Ponto de partida")

    origem = st.selectbox(
        "Selecione onde voce esta",
        options=[""] + LOCAIS_CAMPUS
    )

    st.info(
        "A localizacao automatica pelo GPS sera adicionada "
        "em uma proxima etapa."
    )

    # Exibicao da imagem do mapa
    st.subheader("Visualizacao do campus")

    caminho_mapa = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "mapa_campus.png"
    )

    if os.path.isfile(caminho_mapa) and os.path.getsize(caminho_mapa) > 0:
        st.image(
            caminho_mapa,
            caption="Mapa do Campus",
            use_container_width=True
        )
    else:
        st.warning(
            "Imagem nao encontrada ou vazia. "
            "Verifique se mapa_campus.png esta na pasta views/assets."
        )

    # Botao para buscar destino
    if st.button("Buscar destino", use_container_width=True):

        if not destino:
            st.warning("Selecione o destino desejado.")

        elif not origem:
            st.warning("Selecione seu ponto de partida.")

        elif origem == destino:
            st.warning(
                "O ponto de partida e o destino nao podem ser iguais."
            )

        else:
            st.success(
                f"Destino: {destino}\n\n"
                f"Partida: {origem}"
            )

            st.info(
                "O calculo das rotas e as indicacoes de caminho "
                "serao implementados em uma proxima etapa."
            )
