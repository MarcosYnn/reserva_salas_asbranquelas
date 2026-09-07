import streamlit as st
import database as db

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

# O database.py não tem coluna "proprietario" na tabela salas, então
# não dá pra persistir o dono de cada sala no banco sem alterá-lo.
# Como hoje só existe uma conta de Proprietário (ana), usamos ela como
# dono padrão de qualquer sala que não tenha um dono registrado nesta
# sessão. Isso mantém o app funcional; se um dia existir mais de um
# Proprietário, essa informação vai precisar de uma coluna no banco.
PROPRIETARIO_PADRAO = "ana"

# Mapa (nome da coluna booleana -> rótulo exibido) usado para montar
# o texto "Projetor • Wi-Fi..." que componentes.py já sabe exibir.
MAPA_RECURSOS = [
    ("projetor", "Projetor"),
    ("computador", "Computador"),
    ("internet", "Wi-Fi"),
    ("webcam", "Webcam"),
    ("quadro", "Quadro branco"),
    ("ar_condicionado", "Ar-condicionado"),
]


def _linha_para_dict(linha):
    """Converte uma linha crua do banco (como devolvida por
    db.listar_salas()) no dicionário de sala que o resto do app
    espera: id, nome, capacidade, andar, proprietario, recursos."""

    (
        id_sala, nome, capacidade, localizacao,
        projetor, computador, internet, webcam, quadro, ar_condicionado
    ) = linha

    flags = {
        "projetor": projetor,
        "computador": computador,
        "internet": internet,
        "webcam": webcam,
        "quadro": quadro,
        "ar_condicionado": ar_condicionado,
    }

    recursos = " • ".join(
        rotulo for chave, rotulo in MAPA_RECURSOS if flags[chave]
    ) or "Sem recursos cadastrados"

    return {
        "id": id_sala,
        "nome": nome,
        "capacidade": capacidade,
        "andar": localizacao,
        "proprietario": st.session_state.donos_salas.get(id_sala, PROPRIETARIO_PADRAO),
        "recursos": recursos,
    }


def carregar_salas():
    """Lê as salas do banco (via db.listar_salas()) e devolve já no
    formato de dicionário usado por estado.py/componentes.py/main.py."""
    return [_linha_para_dict(linha) for linha in db.listar_salas()]


def inicializar_estado():
    """Roda uma única vez por sessão. Cria a fonte única de
    verdade dos dados do app (salas e reservas)."""
    if "inicializado" in st.session_state:
        return

    st.session_state.inicializado = True
    st.session_state.usuario = None  # None = ninguém logado ainda

    # dono de cada sala por id, só nesta sessão (ver PROPRIETARIO_PADRAO
    # acima — o banco não tem essa coluna sem alterar database.py)
    st.session_state.donos_salas = {}

    # Garante que a tabela de salas existe no banco SQLite.
    db.criar_tabelas()

    # Na primeira execução (banco vazio), semeia as salas de
    # demonstração direto no banco, em vez de deixá-las só em memória.
    if db.contar_salas() == 0:
        db.cadastrar_sala(
            nome="Sala Executiva", capacidade=12, localizacao="2º andar",
            projetor=True, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de Reunião 01", capacidade=8, localizacao="2º andar",
            projetor=False, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de Reunião 02", capacidade=8, localizacao="2º andar",
            projetor=False, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de Treinamento", capacidade=20, localizacao="3º andar",
            projetor=True, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )

    st.session_state.salas = carregar_salas()

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


def recarregar_salas():
    """Sincroniza st.session_state.salas com o que está no banco.
    Chamar depois de qualquer cadastro/exclusão de sala."""
    st.session_state.salas = carregar_salas()


def adicionar_sala(nome, capacidade, localizacao, proprietario, recursos_marcados):
    """Cadastra uma sala no banco (via db.cadastrar_sala) e atualiza
    a lista em memória.

    recursos_marcados: lista com os nomes das chaves marcadas,
    por exemplo ["projetor", "internet"].
    """
    db.cadastrar_sala(
        nome=nome,
        capacidade=capacidade,
        localizacao=localizacao,
        projetor="projetor" in recursos_marcados,
        computador="computador" in recursos_marcados,
        internet="internet" in recursos_marcados,
        webcam="webcam" in recursos_marcados,
        quadro="quadro" in recursos_marcados,
        ar_condicionado="ar_condicionado" in recursos_marcados,
    )

    # Como o banco não guarda o dono da sala, a sala recém-cadastrada é
    # a de maior id (db.listar_salas() já vem ORDER BY id DESC).
    novo_id = db.listar_salas()[0][0]
    st.session_state.donos_salas[novo_id] = proprietario

    recarregar_salas()


def excluir_sala(sala_id):
    """Exclui uma sala do banco e atualiza a lista em memória."""
    db.excluir_sala(sala_id)
    st.session_state.donos_salas.pop(sala_id, None)
    recarregar_salas()


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