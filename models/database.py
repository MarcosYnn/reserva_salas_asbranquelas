import sqlite3
from pathlib import Path


# Caminho da pasta do banco
DATA_DIR = Path(__file__).parent.parent / "data"

# Cria a pasta caso não exista
DATA_DIR.mkdir(exist_ok=True)

# Caminho do banco
DB_PATH = DATA_DIR / "escritorio.db"


def conectar():
    """Cria uma conexão com o banco de dados."""
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    """Cria as tabelas necessárias para o sistema."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            capacidade INTEGER NOT NULL,
            localizacao TEXT,
            projetor INTEGER DEFAULT 0,
            computador INTEGER DEFAULT 0,
            internet INTEGER DEFAULT 0,
            webcam INTEGER DEFAULT 0,
            quadro INTEGER DEFAULT 0,
            ar_condicionado INTEGER DEFAULT 0
        )
    """)

    # Tabela de usuários do sistema de autenticação. nome_usuario e
    # email são UNIQUE no próprio banco (não só validados na tela),
    # como pedido: impede duplicidade mesmo se duas requisições
    # tentarem cadastrar o mesmo usuário ao mesmo tempo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            nome_completo TEXT,
            senha_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'Locatário',
            ativo INTEGER NOT NULL DEFAULT 1,
            email_confirmado INTEGER NOT NULL DEFAULT 0,
            token_confirmacao TEXT,
            token_redefinicao TEXT,
            data_criacao TEXT NOT NULL
        )
    """)

    # Migração leve para bancos criados antes da coluna "ativo" existir
    # (quem já rodou o app antes desta atualização não perde os dados).
    cursor.execute("PRAGMA table_info(usuarios)")
    colunas_existentes = {linha[1] for linha in cursor.fetchall()}
    if "ativo" not in colunas_existentes:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1")

    conexao.commit()
    conexao.close()


def cadastrar_sala(
    nome,
    capacidade,
    localizacao,
    projetor,
    computador,
    internet,
    webcam,
    quadro,
    ar_condicionado
):
    """Cadastra uma nova sala no banco de dados."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO salas (
            nome,
            capacidade,
            localizacao,
            projetor,
            computador,
            internet,
            webcam,
            quadro,
            ar_condicionado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        capacidade,
        localizacao,
        int(projetor),
        int(computador),
        int(internet),
        int(webcam),
        int(quadro),
        int(ar_condicionado)
    ))

    conexao.commit()
    conexao.close()


def listar_salas():
    """Retorna todas as salas cadastradas."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            capacidade,
            localizacao,
            projetor,
            computador,
            internet,
            webcam,
            quadro,
            ar_condicionado
        FROM salas
        ORDER BY id DESC
    """)

    salas = cursor.fetchall()

    conexao.close()

    return salas


def excluir_sala(id_sala):
    """Exclui uma sala pelo ID."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM salas WHERE id = ?",
        (id_sala,)
    )

    conexao.commit()
    conexao.close()


def contar_salas():
    """Retorna a quantidade de salas cadastradas."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM salas")

    quantidade = cursor.fetchone()[0]

    conexao.close()

    return quantidade


# ==========================================
# USUÁRIOS (autenticação)
# ==========================================

COLUNAS_USUARIO = (
    "id", "nome_usuario", "email", "nome_completo", "senha_hash", "salt",
    "tipo", "ativo", "email_confirmado", "token_confirmacao",
    "token_redefinicao", "data_criacao"
)


def _linha_usuario_para_dict(linha):
    if linha is None:
        return None
    return dict(zip(COLUNAS_USUARIO, linha))


def criar_usuario(
    nome_usuario,
    email,
    nome_completo,
    senha_hash,
    salt,
    tipo,
    token_confirmacao,
    data_criacao,
    email_confirmado=False,
    ativo=True
):
    """Insere um novo usuário no banco. Levanta sqlite3.IntegrityError
    se nome_usuario ou email já existirem (restrição UNIQUE no schema)."""

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (
                nome_usuario, email, nome_completo, senha_hash, salt,
                tipo, ativo, email_confirmado, token_confirmacao,
                token_redefinicao, data_criacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)
        """, (
            nome_usuario, email, nome_completo, senha_hash, salt,
            tipo, int(ativo), int(email_confirmado), token_confirmacao, data_criacao
        ))
        conexao.commit()
        novo_id = cursor.lastrowid
    finally:
        conexao.close()

    return novo_id


def buscar_usuario_por_nome(nome_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE nome_usuario = ?", (nome_usuario,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE email = ?", (email,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def buscar_usuario_por_login(identificador):
    """Busca por nome_usuario OU email — usado na tela de login,
    que aceita as duas formas de identificação."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE nome_usuario = ? OR email = ?",
        (identificador, identificador)
    )
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE id = ?", (usuario_id,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def buscar_usuario_por_token_confirmacao(token):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE token_confirmacao = ?", (token,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def buscar_usuario_por_token_redefinicao(token):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios WHERE token_redefinicao = ?", (token,))
    linha = cursor.fetchone()
    conexao.close()
    return _linha_usuario_para_dict(linha)


def confirmar_email_usuario(usuario_id):
    """Marca o e-mail como confirmado e limpa o token usado."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET email_confirmado = 1, token_confirmacao = NULL WHERE id = ?",
        (usuario_id,)
    )
    conexao.commit()
    conexao.close()


def definir_token_redefinicao(usuario_id, token):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET token_redefinicao = ? WHERE id = ?",
        (token, usuario_id)
    )
    conexao.commit()
    conexao.close()


def atualizar_senha_usuario(usuario_id, senha_hash, salt):
    """Atualiza a senha e limpa o token de redefinição (uso único)."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET senha_hash = ?, salt = ?, token_redefinicao = NULL WHERE id = ?",
        (senha_hash, salt, usuario_id)
    )
    conexao.commit()
    conexao.close()


def definir_tipo_usuario(usuario_id, tipo):
    """Usado pelo painel de administração para promover/rebaixar contas."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (tipo, usuario_id))
    conexao.commit()
    conexao.close()


def definir_ativo_usuario(usuario_id, ativo):
    """Bloqueia (ativo=False) ou reativa (ativo=True) uma conta.
    Uma conta bloqueada não consegue mais fazer login."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET ativo = ? WHERE id = ?", (int(ativo), usuario_id))
    conexao.commit()
    conexao.close()


def excluir_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conexao.commit()
    conexao.close()


def listar_usuarios():
    """Retorna todos os usuários (usado no painel de administração)."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_usuario, email, nome_completo, senha_hash, salt, tipo, ativo, email_confirmado, token_confirmacao, token_redefinicao, data_criacao FROM usuarios ORDER BY id ASC")
    linhas = cursor.fetchall()
    conexao.close()
    return [_linha_usuario_para_dict(linha) for linha in linhas]


def contar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    quantidade = cursor.fetchone()[0]
    conexao.close()
    return quantidade