import os
import streamlit as st
from utils.estado import fazer_login


def pagina_login():
    # DivisÃ£o principal: Painel Esquerdo (ApresentaÃ§Ã£o) | Painel Direito (Login)
    col_esquerda, col_direita = st.columns([1.1, 1], gap="large")

    # --- PAINEL ESQUERDO (ApresentaÃ§Ã£o) ---
    with col_esquerda:
        # CabeÃ§alho com LogÃ³tipo
        col_logo, col_titulo = st.columns([0.28, 0.72], vertical_alignment="center")
        with col_logo:
            diretorio_base = os.path.dirname(os.path.abspath(__file__))
            caminho_logo = os.path.join(diretorio_base, "assets", "logo.png")

            if os.path.exists(caminho_logo):
                st.image(caminho_logo, width=85)  # Logo aumentada
            else:
                st.text("ðŸ¢")

        with col_titulo:
            st.markdown(
                '<div style="line-height: 1.2;">'
                '<span style="font-size: 22px; font-weight: bold; color: #0f172a;">Reserva de Salas</span><br>'
                '<span style="font-size: 13px; color: #475569; font-weight: 500;">Sistema AcadÃ©mico</span>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # TÃ­tulo principal em Preto e Azul
        st.markdown(
            '<h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 10px;">'
            'Mais que salas,<br><span style="color: #2563eb;">oportunidades.</span>'
            "</h1>",
            unsafe_allow_html=True,
        )

        # SubtÃ­tulo legÃ­vel em cinza escuro/preto
        st.markdown(
            '<p style="color: #334155; font-size: 15px; line-height: 1.5; font-weight: 400;">'
            "Reserve espaÃ§os da sua instituiÃ§Ã£o de forma simples, rÃ¡pida e segura. "
            "Aqui, cada sala Ã© um passo para grandes ideias."
            "</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # CartÃµes de categorias em tons claros com texto escuro
        cat1, cat2, cat3, cat4 = st.columns(4)
        with cat1:
            st.markdown(
                '<div style="text-align: center; padding: 12px 6px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px;">'
                '<span style="font-size: 22px;">ðŸ’»</span><br>'
                '<span style="font-size: 12px; color: #0f172a; font-weight: 600;">Salas de Aula</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        with cat2:
            st.markdown(
                '<div style="text-align: center; padding: 12px 6px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px;">'
                '<span style="font-size: 22px;">ðŸ§ª</span><br>'
                '<span style="font-size: 12px; color: #0f172a; font-weight: 600;">LaboratÃ³rios</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        with cat3:
            st.markdown(
                '<div style="text-align: center; padding: 12px 6px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px;">'
                '<span style="font-size: 22px;">ðŸ› ï¸</span><br>'
                '<span style="font-size: 12px; color: #0f172a; font-weight: 600;">Oficinas</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        with cat4:
            st.markdown(
                '<div style="text-align: center; padding: 12px 6px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px;">'
                '<span style="font-size: 22px;">ðŸŽ­</span><br>'
                '<span style="font-size: 12px; color: #0f172a; font-weight: 600;">AuditÃ³rios</span>'
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size: 11px; letter-spacing: 1.5px; color: #475569; font-weight: 700;">'
            "TECNOLOGIA A SERVIÃ‡O DA SUA JORNADA ACADÃ‰MICA."
            "</p>",
            unsafe_allow_html=True,
        )

    # --- PAINEL DIREITO (FormulÃ¡rio) ---
    with col_direita:
        st.markdown(
            '<div style="text-align: right; color: #475569; font-size: 12px; margin-bottom: 20px; font-weight: 600;">'
            "ðŸ”’ Acesso Restrito"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<h2 style="font-size: 26px; font-weight: bold; color: #0f172a; margin-bottom: 4px;">'
            "Bem-vindo de volta!"
            "</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color: #475569; font-size: 14px; margin-bottom: 24px;">'
            "FaÃ§a login para continuar com a reserva de salas."
            "</p>",
            unsafe_allow_html=True,
        )

        with st.form("form_login_moderno"):
            login_input = st.text_input(
                "UsuÃ¡rio", placeholder="Digite seu usuÃ¡rio"
            )

            senha_input = st.text_input(
                "Senha", type="password", placeholder="Digite sua senha"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            entrar = st.form_submit_button(
                "âž” Entrar", type="primary", use_container_width=True
            )

        if entrar:
            if fazer_login(login_input, senha_input):
                st.rerun()
            else:
                st.error("UsuÃ¡rio ou senha invÃ¡lidos.")

        with st.expander("Contas de demonstraÃ§Ã£o"):
            st.caption("**LocatÃ¡rio:** usuÃ¡rio `marcos` Â· senha `1234`")
            st.caption("**ProprietÃ¡rio:** usuÃ¡rio `ana` Â· senha `1234`")
