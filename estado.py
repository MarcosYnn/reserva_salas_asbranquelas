import streamlit as st

# ==========================================
# USUÁRIOS CADASTRADOS (mock de autenticação)
# ==========================================
# Em produção isso viria de um banco de dados com senha
# criptografada. Aqui fica só a estrutura para separar
# contas de Locatário e de Proprietário de fato.

USUARIOS = {
    "marcos": {"senha": "1234", "nome": "Marcos Silva", "tipo": "Locatário"},
    "fernanda": {"senha": "1234", "nome": "Fernanda Reis", "tipo": "Locatário"},
    "ana": {"senha": "1234", "nome": "Ana Souza", "tipo": "Proprietário"},
}


def inicializar_estado():
    """Roda uma única vez por sessão. Cria a fonte única de
    verdade dos dados do app (salas e reservas)."""
    if "inicializado" in st.session_state:
        return

    st.session_state.inicializado = True
    st.session_state.usuario = None  # None = ninguém logado ainda

    st.session_state.salas = [
        {"id": 1, "nome": "Sala Executiva", "capacidade": 12,
         "recursos": "TV • Projetor • Wi-Fi", "andar": "2º andar",
         "proprietario": "ana"},
        {"id": 2, "nome": "Sala de Reunião 01", "capacidade": 8,
         "recursos": "TV • Wi-Fi", "andar": "2º andar",
         "proprietario": "ana"},
        {"id": 3, "nome": "Sala de Reunião 02", "capacidade": 8,
         "recursos": "TV • Wi-Fi", "andar": "2º andar",
         "proprietario": "ana"},
        {"id": 4, "nome": "Sala de Treinamento", "capacidade": 20,
         "recursos": "Projetor • Wi-Fi", "andar": "3º andar",
         "proprietario": "ana"},
    ]

    st.session_state.reservas = [
        {"sala_id": 3, "cliente": "Marcos Silva", "data": "17/08/2026",
         "horario": "14:00 - 16:00", "status": "Confirmada"},
        {"sala_id": 2, "cliente": "Marcos Silva", "data": "19/08/2026",
         "horario": "09:00 - 11:00", "status": "Confirmada"},
        {"sala_id": 4, "cliente": "Marcos Silva", "data": "21/08/2026",
         "horario": "15:00 - 17:00", "status": "Pendente"},
        {"sala_id": 1, "cliente": "Fernanda Reis", "data": "18/08/2026",
         "horario": "10:00 - 12:00", "status": "Confirmada"},
        {"sala_id": 4, "cliente": "Carlos Lima", "data": "19/08/2026",
         "horario": "13:00 - 15:00", "status": "Pendente"},
    ]

    st.session_state.favoritos = set()
    st.session_state.resultado_busca = None


def sala_por_id(sala_id):
    return next(s for s in st.session_state.salas if s["id"] == sala_id)


def reservas_de(cliente_nome):
    return [r for r in st.session_state.reservas if r["cliente"] == cliente_nome]


def salas_de(proprietario_login):
    return [s for s in st.session_state.salas if s["proprietario"] == proprietario_login]


def reservas_das_salas(sala_ids):
    return [r for r in st.session_state.reservas if r["sala_id"] in sala_ids]


def usuario_logado():
    return st.session_state.usuario


def fazer_login(login, senha):
    dados = USUARIOS.get(login)
    if dados and dados["senha"] == senha:
        st.session_state.usuario = {"login": login, **dados}
        return True
    return False


def fazer_logout():
    st.session_state.usuario = None
