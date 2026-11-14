
import os
import streamlit as st


def pagina_mapa_campus(usuario):

    st.title("Mapa do Campus")
    st.write("Encontre salas e outros espacos dentro do campus.")

    st.divider()

    # Escolha do destino
    st.subheader("Para onde deseja ir?")

    destino = st.text_input(
        "Digite o nome da sala ou local desejado",
        placeholder="Ex.: Laboratorio de Informatica"
    )

    # Ponto de partida
    st.subheader("Ponto de partida")

    origem = st.text_input(
        "Informe onde voce esta no campus",
        placeholder="Ex.: Entrada principal"
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

    if os.path.exists(caminho_mapa):
        st.image(
            caminho_mapa,
            caption="Mapa do Campus",
            use_container_width=True
        )
    else:
        st.warning(
            "Imagem nao encontrada. "
            "Verifique se mapa_campus.png esta na pasta views/assets."
        )

    # Botao para buscar destino
    if st.button("Buscar destino", use_container_width=True):

        if not destino:
            st.warning("Informe o destino desejado.")

        elif not origem:
            st.warning("Informe seu ponto de partida.")

        else:
            st.success(
                f"Destino: {destino}\n\n"
                f"Partida: {origem}"
            )

            st.info(
                "O calculo das rotas e as indicacoes de caminho "
                "serao implementados em uma proxima etapa."
            )
