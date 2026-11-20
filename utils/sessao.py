import streamlit as st


def limpar_dados_usuario():
    """Preserva só o estado técnico, nunca dados ou widgets da conta anterior."""
    for chave in list(st.session_state):
        if chave not in {"inicializado_firebase", "salas"}:
            del st.session_state[chave]
    st.session_state.usuario = None
    st.session_state.favoritos = set()
    st.session_state.resultado_busca = None
