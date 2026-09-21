"""
Script para criar (ou atualizar a senha d)o usuÃ¡rio administrador.

NÃ£o existe senha de administrador fixa no cÃ³digo â€” este script lÃª as
credenciais de variÃ¡veis de ambiente (ADMIN_USERNAME, ADMIN_EMAIL,
ADMIN_PASSWORD) e, se alguma nÃ£o estiver definida, pergunta na hora
pelo terminal (a senha Ã© digitada sem aparecer na tela).

Uso:
    # via variÃ¡veis de ambiente
    export ADMIN_USERNAME=admin
    export ADMIN_EMAIL=admin@suaempresa.com
    export ADMIN_PASSWORD='SenhaForte123'
    python criar_admin.py

    # ou, sem definir nada antes, o script pergunta interativamente:
    python criar_admin.py
"""

import getpass
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv nÃ£o instalado: use variÃ¡veis de ambiente do sistema

from models import database as db
from utils.estado import criar_ou_atualizar_admin


def main():
    db.criar_tabelas()

    nome_usuario = os.environ.get("ADMIN_USERNAME") or input("Nome de usuÃ¡rio do administrador: ").strip()
    email = os.environ.get("ADMIN_EMAIL") or input("E-mail do administrador: ").strip()
    senha = os.environ.get("ADMIN_PASSWORD") or getpass.getpass("Senha do administrador: ")

    sucesso, mensagem = criar_ou_atualizar_admin(nome_usuario, email, senha)

    print(mensagem)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()

