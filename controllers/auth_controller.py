"""
Funções de apoio à autenticação: hash de senha, geração de tokens,
validação de dados e envio de e-mail de confirmação/redefinição.

Todas as credenciais de e-mail (SMTP) vêm de variáveis de ambiente —
nunca ficam escritas no código. Veja o arquivo .env.example para a
lista completa de variáveis aceitas.
"""

import hashlib
import hmac
import os
import re
import secrets
import smtplib
from email.message import EmailMessage
from pathlib import Path


# ==========================================
# HASH DE SENHA (PBKDF2-HMAC-SHA256, biblioteca padrão do Python,
# sem precisar instalar bcrypt/passlib)
# ==========================================

ITERACOES_PBKDF2 = 200_000


def gerar_hash_senha(senha):
    """Gera um salt aleatório e retorna (hash_hex, salt_hex)."""
    salt = secrets.token_hex(16)
    hash_hex = _derivar_hash(senha, salt)
    return hash_hex, salt


def verificar_senha(senha, hash_hex, salt_hex):
    """Confere a senha digitada contra o hash salvo, usando
    comparação em tempo constante (evita timing attack)."""
    hash_calculado = _derivar_hash(senha, salt_hex)
    return hmac.compare_digest(hash_calculado, hash_hex)


def _derivar_hash(senha, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        bytes.fromhex(salt_hex),
        ITERACOES_PBKDF2
    ).hex()


# ==========================================
# TOKENS (confirmação de e-mail / redefinição de senha)
# ==========================================

def gerar_token():
    return secrets.token_urlsafe(32)


# ==========================================
# VALIDAÇÕES
# ==========================================

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REGEX_USUARIO = re.compile(r"^[a-zA-Z0-9_.]{3,30}$")


def validar_email(email):
    return bool(REGEX_EMAIL.match(email or ""))


def validar_nome_usuario(nome_usuario):
    """Entre 3 e 30 caracteres, apenas letras, números, ponto e
    underline (evita nomes de usuário que quebrem a URL/consulta)."""
    return bool(REGEX_USUARIO.match(nome_usuario or ""))


def validar_senha_forte(senha):
    """Regras mínimas: 8+ caracteres, ao menos 1 letra maiúscula,
    1 minúscula e 1 número. Retorna (ok: bool, mensagem: str)."""
    senha = senha or ""
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve ter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", senha):
        return False, "A senha deve ter pelo menos uma letra minúscula."
    if not re.search(r"[0-9]", senha):
        return False, "A senha deve ter pelo menos um número."
    return True, ""


# ==========================================
# ENVIO DE E-MAIL
# ==========================================
# Variáveis de ambiente esperadas (ver .env.example):
#   SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
#   SMTP_FROM, SMTP_USE_TLS, APP_BASE_URL
#
# Se SMTP_HOST não estiver configurado (ex.: ambiente de
# desenvolvimento sem servidor de e-mail), o "envio" cai para um
# arquivo local data/emails_enviados.log, só para você conseguir
# testar o fluxo de confirmação sem precisar de um SMTP de verdade.

def _pasta_dados():
    caminho = Path(__file__).parent.parent / "data"
    caminho.mkdir(exist_ok=True)
    return caminho


def _registrar_email_local(destinatario, assunto, corpo):
    caminho_log = _pasta_dados() / "emails_enviados.log"
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write("=" * 60 + "\n")
        arquivo.write(f"Para: {destinatario}\nAssunto: {assunto}\n\n{corpo}\n\n")


def enviar_email(destinatario, assunto, corpo_texto):
    """Envia um e-mail via SMTP (se configurado) ou registra
    localmente em data/emails_enviados.log (modo desenvolvimento).
    Retorna True se enviou de fato por SMTP, False se só registrou
    localmente ou se o envio falhou."""

    smtp_host = os.environ.get("SMTP_HOST")

    if not smtp_host:
        _registrar_email_local(destinatario, assunto, corpo_texto)
        return False

    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM", smtp_user)
    usar_tls = os.environ.get("SMTP_USE_TLS", "true").lower() != "false"

    mensagem = EmailMessage()
    mensagem["Subject"] = assunto
    mensagem["From"] = smtp_from
    mensagem["To"] = destinatario
    mensagem.set_content(corpo_texto)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as servidor:
            if usar_tls:
                servidor.starttls()
            if smtp_user and smtp_password:
                servidor.login(smtp_user, smtp_password)
            servidor.send_message(mensagem)
        return True
    except Exception:
        # Não deixa o cadastro quebrar por causa do e-mail — registra
        # localmente como fallback e segue o fluxo normalmente.
        _registrar_email_local(destinatario, assunto, corpo_texto)
        return False


def montar_link_confirmacao(token):
    base = os.environ.get("APP_BASE_URL", "http://localhost:8501")
    return f"{base}?confirmar={token}"


def montar_link_redefinicao(token):
    base = os.environ.get("APP_BASE_URL", "http://localhost:8501")
    return f"{base}?redefinir={token}"


def enviar_email_confirmacao(destinatario, nome_usuario, token):
    link = montar_link_confirmacao(token)
    corpo = (
        f"Olá, {nome_usuario}!\n\n"
        "Obrigado por se cadastrar no Reserva de Salas.\n"
        "Para ativar sua conta, clique no link abaixo:\n\n"
        f"{link}\n\n"
        "Se você não fez esse cadastro, ignore este e-mail."
    )
    return enviar_email(destinatario, "Confirme seu e-mail — Reserva de Salas", corpo)


def enviar_email_redefinicao(destinatario, nome_usuario, token):
    link = montar_link_redefinicao(token)
    corpo = (
        f"Olá, {nome_usuario}!\n\n"
        "Recebemos um pedido de redefinição de senha para sua conta.\n"
        "Para criar uma nova senha, clique no link abaixo:\n\n"
        f"{link}\n\n"
        "Se você não pediu isso, ignore este e-mail — sua senha atual continua válida."
    )
    return enviar_email(destinatario, "Redefinição de senha — Reserva de Salas", corpo)
