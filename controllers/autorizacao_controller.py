"""
Autorização centralizada — separada da autenticação (que fica em
estado.py/auth.py).

A ideia deste módulo: NENHUMA página protegida deve confiar apenas em
"o menu não mostrou o botão". Toda função de página em main.py que
exige um tipo de conta específico chama exigir_tipo(...) logo na
primeira linha. Se o usuário não tiver permissão, a página para ali
mesmo (st.stop()) e mostra uma mensagem de acesso negado — mesmo que,
hipoteticamente, alguém consiga chamar a função por outro caminho.

Isso é o que garante que um Locatário não acesse a área administrativa
"manipulando" o estado da sessão — a verificação acontece no backend
(dentro da função Python), não só na hora de montar o menu lateral.
"""

import streamlit as st


def usuario_autenticado():
    """True se existir alguém logado nesta sessão."""
    return st.session_state.get("usuario") is not None


def exigir_autenticacao():
    """Interrompe a renderização da página se ninguém estiver logado.
    Use no topo de qualquer função que só faça sentido autenticada."""
    if not usuario_autenticado():
        st.error("Você precisa estar autenticado para acessar esta página.")
        st.stop()


def exigir_tipo(usuario, tipos_permitidos):
    """Interrompe a renderização da página se o usuário não estiver
    autenticado OU se o tipo da conta dele não estiver na lista de
    tipos permitidos para essa página.

    usuario: o dicionário de st.session_state.usuario (ou None).
    tipos_permitidos: lista/tupla com os tipos que podem acessar,
                       ex.: [TIPO_ADMIN] ou [TIPO_PROPRIETARIO, TIPO_ADMIN].
    """
    if usuario is None:
        st.error("Você precisa estar autenticado para acessar esta página.")
        st.stop()

    if usuario["tipo"] not in tipos_permitidos:
        st.error(
            f"Acesso negado: sua conta é do tipo **{usuario['tipo']}** e "
            "não tem permissão para acessar esta página."
        )
        st.stop()
