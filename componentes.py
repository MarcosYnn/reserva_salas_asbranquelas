import streamlit as st
from estado import sala_por_id


def injetar_css():
    st.markdown("""
    <style>
        .stApp { background-color: #f7f8fc; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #171a4a 0%, #272c70 100%);
        }
        section[data-testid="stSidebar"] * { color: white; }

        .titulo { font-size: 32px; font-weight: 700; color: #15182f; margin-bottom: 5px; }
        .subtitulo { font-size: 16px; color: #6b7280; margin-bottom: 25px; }

        .card {
            background-color: white; border-radius: 14px; padding: 20px;
            border: 1px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            min-height: 120px;
        }
        .card-titulo { color: #6b7280; font-size: 14px; margin-bottom: 8px; }
        .card-numero { font-size: 28px; font-weight: 700; color: #15182f; }
        .card-info { color: #22a06b; font-size: 13px; margin-top: 5px; }

        .secao {
            background-color: white; border-radius: 14px; padding: 22px;
            border: 1px solid #e5e7eb; margin-top: 20px;
        }
        .secao-titulo { font-size: 20px; font-weight: 700; color: #15182f; margin-bottom: 18px; }

        .reserva {
            background-color: #fafbff; border: 1px solid #e5e7eb; border-radius: 10px;
            padding: 15px; margin-bottom: 10px;
        }
        .reserva-titulo { font-weight: 700; color: #15182f; }
        .reserva-info { color: #6b7280; font-size: 14px; margin-top: 5px; }

        .sala {
            background-color: white; border: 1px solid #e5e7eb; border-radius: 12px;
            padding: 18px; margin-bottom: 10px;
        }
        .sala-titulo { font-size: 18px; font-weight: 700; color: #15182f; }
        .sala-info { color: #6b7280; font-size: 14px; margin-top: 6px; }
    </style>
    """, unsafe_allow_html=True)


def render_card(titulo, numero, info):
    st.markdown(f"""
    <div class="card">
        <div class="card-titulo">{titulo}</div>
        <div class="card-numero">{numero}</div>
        <div class="card-info">{info}</div>
    </div>
    """, unsafe_allow_html=True)


def render_secao_titulo(texto):
    st.markdown(f"""
    <div class="secao">
        <div class="secao-titulo">{texto}</div>
    </div>
    """, unsafe_allow_html=True)


def render_lista_reservas(lista, mostrar_cliente=False):
    if not lista:
        st.caption("Nenhuma reserva encontrada.")
        return

    for r in lista:
        sala = sala_por_id(r["sala_id"])
        cols = st.columns([2, 2, 1.2, 1.5, 1]) if mostrar_cliente else st.columns([2, 1.2, 1.5, 1])
        i = 0
        with cols[i]:
            st.write(f"**{sala['nome']}**")
        i += 1
        if mostrar_cliente:
            with cols[i]:
                st.write(r["cliente"])
            i += 1
        with cols[i]:
            st.write(r["data"])
        i += 1
        with cols[i]:
            st.write(r["horario"])
        i += 1
        with cols[i]:
            if r["status"] == "Confirmada":
                st.success(r["status"])
            else:
                st.warning(r["status"])


def render_sala_card(sala, coluna, contexto, usuario_atual_nome):
    with coluna:
        favoritada = sala["id"] in st.session_state.favoritos
        st.markdown(f"""
        <div class="sala">
            <div class="sala-titulo">🏢 {sala['nome']}</div>
            <div class="sala-info">👥 Capacidade: {sala['capacidade']} pessoas</div>
            <div class="sala-info">🖥️ {sala['recursos']}</div>
            <div class="sala-info">📍 {sala['andar']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_reservar, col_fav = st.columns([2, 1])
        with col_reservar:
            if st.button("Reservar", key=f"reservar_{contexto}_{sala['id']}"):
                st.session_state.reservas.append({
                    "sala_id": sala["id"],
                    "cliente": usuario_atual_nome,
                    "data": st.session_state.get("busca_data_fmt", "A definir"),
                    "horario": st.session_state.get("busca_horario_fmt", "A definir"),
                    "status": "Pendente",
                })
                st.success(f"{sala['nome']} reservada! Veja em 'Minhas Reservas'.")
        with col_fav:
            rotulo = "💛" if favoritada else "🤍"
            if st.button(rotulo, key=f"fav_{contexto}_{sala['id']}"):
                if favoritada:
                    st.session_state.favoritos.discard(sala["id"])
                else:
                    st.session_state.favoritos.add(sala["id"])
                st.rerun()
