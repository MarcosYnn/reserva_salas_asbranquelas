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
