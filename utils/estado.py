import os
import sqlite3
from datetime import datetime

import streamlit as st

from models import database as db
from controllers import auth_controller as auth


# ==========================================
# TIPOS DE CONTA
# ==========================================
TIPO_LOCATARIO = "LocatÃ¡rio"
TIPO_PROPRIETARIO = "ProprietÃ¡rio"
TIPO_ADMIN = "Administrador"

# ==========================================
# ADMIN PADRÃƒO (pronto para uso, sem precisar configurar nada)
# ==========================================
# Se as variÃ¡veis de ambiente ADMIN_USERNAME/ADMIN_EMAIL/ADMIN_PASSWORD
# nÃ£o estiverem definidas, o sistema cria automaticamente esta conta na
# primeira execuÃ§Ã£o. Para um projeto em produÃ§Ã£o, defina essas 3
# variÃ¡veis (no .env ou no ambiente do servidor) com valores prÃ³prios â€”
# elas sempre tÃªm prioridade sobre estes valores padrÃ£o.
ADMIN_USUARIO_PADRAO = "admin"
ADMIN_EMAIL_PADRAO = "admin@escritorio.com"
ADMIN_SENHA_PADRAO = "Admin@123"  # precisa de maiÃºscula+minÃºscula+nÃºmero (regra de senha forte)

# O database.py nÃ£o tem coluna "proprietario" na tabela salas, entÃ£o
# nÃ£o dÃ¡ pra persistir o dono de cada sala no banco sem alterÃ¡-lo
# (isso foi mantido de propÃ³sito da etapa anterior). Como hoje sÃ³
# existe uma conta de ProprietÃ¡rio de demonstraÃ§Ã£o (ana), usamos ela
# como dono padrÃ£o de qualquer sala sem dono registrado nesta sessÃ£o.
PROPRIETARIO_PADRAO = "ana"

MAPA_RECURSOS = [
    ("projetor", "Projetor"),
    ("computador", "Computador"),
    ("internet", "Wi-Fi"),
    ("webcam", "Webcam"),
    ("quadro", "Quadro branco"),
    ("ar_condicionado", "Ar-condicionado"),
]


# ==========================================
# SALAS (mesma lÃ³gica jÃ¡ usada antes, sem mudanÃ§as de comportamento)
# ==========================================

def _linha_sala_para_dict(linha):
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

    recursos = " â€¢ ".join(
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
    return [_linha_sala_para_dict(linha) for linha in db.listar_salas()]


def recarregar_salas():
    st.session_state.salas = carregar_salas()


def adicionar_sala(nome, capacidade, localizacao, proprietario, recursos_marcados):
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
    novo_id = db.listar_salas()[0][0]
    st.session_state.donos_salas[novo_id] = proprietario
    recarregar_salas()


def excluir_sala(sala_id):
    db.excluir_sala(sala_id)
    st.session_state.donos_salas.pop(sala_id, None)
    recarregar_salas()


def sala_por_id(sala_id):
    return next(s for s in st.session_state.salas if s["id"] == sala_id)


def salas_de(proprietario_login):
    return [s for s in st.session_state.salas if s["proprietario"] == proprietario_login]


# ==========================================
# RESERVAS (segue em memÃ³ria â€” o database.py nÃ£o tem tabela de
# reservas; fora do escopo desta tarefa de autenticaÃ§Ã£o)
# ==========================================

def reservas_de(cliente_nome):
    return [r for r in st.session_state.reservas if r["cliente"] == cliente_nome]


def reservas_das_salas(sala_ids):
    return [r for r in st.session_state.reservas if r["sala_id"] in sala_ids]


# ==========================================
# SESSÃƒO / AUTENTICAÃ‡ÃƒO
# ==========================================

def _usuario_db_para_sessao(usuario_db):
    """Converte a linha de usuÃ¡rio do banco no dicionÃ¡rio que o
    resto do app usa em st.session_state.usuario. MantÃ©m as chaves
    "login", "nome" e "tipo" que main.py/componentes.py jÃ¡ esperam."""
    return {
        "id": usuario_db["id"],
        "login": usuario_db["nome_usuario"],
        "email": usuario_db["email"],
        "nome": usuario_db["nome_completo"] or usuario_db["nome_usuario"],
        "tipo": usuario_db["tipo"],
        "eh_admin": usuario_db["tipo"] == TIPO_ADMIN,
    }


def usuario_logado():
    return st.session_state.usuario


def cadastrar_usuario(nome_usuario, email, nome_completo, senha, confirmar_senha, tipo=TIPO_LOCATARIO):
    """Valida e cria uma nova conta (nÃ£o confirmada) e dispara o
    e-mail de confirmaÃ§Ã£o. Retorna (sucesso: bool, mensagem: str)."""

    nome_usuario = (nome_usuario or "").strip()
    email = (email or "").strip().lower()
    nome_completo = (nome_completo or "").strip()

    if not nome_usuario or not email or not nome_completo or not senha or not confirmar_senha:
        return False, "Preencha todos os campos."

    if not auth.validar_nome_usuario(nome_usuario):
        return False, "Nome de usuÃ¡rio invÃ¡lido: use de 3 a 30 letras, nÃºmeros, ponto ou underline."

    if not auth.validar_email(email):
        return False, "Informe um e-mail vÃ¡lido."

    if senha != confirmar_senha:
        return False, "As senhas nÃ£o coincidem."

    senha_ok, mensagem_senha = auth.validar_senha_forte(senha)
    if not senha_ok:
        return False, mensagem_senha

    if db.buscar_usuario_por_nome(nome_usuario):
        return False, "Esse nome de usuÃ¡rio jÃ¡ estÃ¡ em uso."

    if db.buscar_usuario_por_email(email):
        return False, "JÃ¡ existe uma conta cadastrada com esse e-mail."

    senha_hash, salt = auth.gerar_hash_senha(senha)
    token = auth.gerar_token()

    try:
        db.criar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            nome_completo=nome_completo,
            senha_hash=senha_hash,
            salt=salt,
            tipo=tipo,
            token_confirmacao=token,
            data_criacao=datetime.now().isoformat(timespec="seconds"),
            email_confirmado=False,
        )
    except sqlite3.IntegrityError:
        # ProteÃ§Ã£o extra caso duas tentativas cheguem ao mesmo tempo â€”
        # a restriÃ§Ã£o UNIQUE do banco garante que nunca haverÃ¡ duplicata.
        return False, "Nome de usuário ou e-mail já cadastrado."

    enviado_por_smtp = auth.enviar_email_confirmacao(email, nome_usuario, token)
    if enviado_por_smtp:
        return True, "Conta criada! Enviamos um e-mail de confirmação — confirme para poder entrar."
    return True, (
        "Conta criada! Não há um servidor de e-mail configurado neste ambiente, "
        "então o link de confirmação foi salvo em data/emails_enviados.log para teste."
    )


def fazer_login(identificador, senha):
    """identificador pode ser nome de usuário OU e-mail.
    Retorna (sucesso: bool, mensagem: str)."""

    identificador = (identificador or "").strip()
    usuario_db = db.buscar_usuario_por_login(identificador)

    # Mensagem genÃ©rica em ambos os casos (usuÃ¡rio inexistente ou
    # senha errada) para nÃ£o revelar se um usuÃ¡rio existe ou nÃ£o.
    if not usuario_db or not auth.verificar_senha(senha or "", usuario_db["senha_hash"], usuario_db["salt"]):
        return False, "Usuário/e-mail ou senha inválidos."

    if not usuario_db["email_confirmado"]:
        return False, "Confirme seu e-mail antes de entrar. Verifique sua caixa de entrada."

    if not usuario_db["ativo"]:
        return False, "Sua conta foi desativada. Entre em contato com um administrador."

    st.session_state.usuario = _usuario_db_para_sessao(usuario_db)
    return True, "Login efetuado com sucesso."


def fazer_logout():
    st.session_state.usuario = None


def confirmar_email_via_token(token):
    """Usado quando o usuário abre o link recebido por e-mail.
    Retorna (sucesso: bool, mensagem: str)."""
    if not token:
        return False, "Link de confirmação inválido."

    usuario_db = db.buscar_usuario_por_token_confirmacao(token)
    if not usuario_db:
        return False, "Link de confirmação inválido ou já utilizado."

    db.confirmar_email_usuario(usuario_db["id"])
    return True, "E-mail confirmado com sucesso! Voce já pode entrar."


def solicitar_redefinicao_senha(email):
    """Gera um token de redefinição e envia por e-mail.
    Retorna (sucesso: bool, mensagem: str)."""
    email = (email or "").strip().lower()
    usuario_db = db.buscar_usuario_por_email(email)
    if not usuario_db:
        return False, "Não encontramos nenhuma conta com esse e-mail."

    token = auth.gerar_token()
    db.definir_token_redefinicao(usuario_db["id"], token)
    auth.enviar_email_redefinicao(email, usuario_db["nome_usuario"], token)
    return True, "Se o e-mail existir, enviamos um link de redefinição de senha."


def redefinir_senha_via_token(token, nova_senha, confirmar_nova_senha):
    """Usado na tela acessada pelo link de redefinição.
    Retorna (sucesso: bool, mensagem: str)."""
    if not token:
        return False, "Link de redefinição inválido."

    usuario_db = db.buscar_usuario_por_token_redefinicao(token)
    if not usuario_db:
        return False, "Link de redefinição inválido ou já utilizado."

    if nova_senha != confirmar_nova_senha:
        return False, "As senhas não coincidem."

    senha_ok, mensagem_senha = auth.validar_senha_forte(nova_senha)
    if not senha_ok:
        return False, mensagem_senha

    senha_hash, salt = auth.gerar_hash_senha(nova_senha)
    db.atualizar_senha_usuario(usuario_db["id"], senha_hash, salt)
    return True, "Senha redefinida com sucesso! Já pode entrar com a nova senha."


# ==========================================
# ADMINISTRAÇÃO
# ==========================================

def criar_ou_atualizar_admin(nome_usuario, email, senha):
    """Cria a conta de administrador (já confirmada, sem precisar de
    e-mail) ou atualiza a senha se ela já existir. Usado tanto pelo
    script criar_admin.py quanto pela inicialização via variáveis de
    ambiente. Retorna (sucesso: bool, mensagem: str)."""

    nome_usuario = (nome_usuario or "").strip()
    email = (email or "").strip().lower()

    if not nome_usuario or not email or not senha:
        return False, "ADMIN_USERNAME, ADMIN_EMAIL e ADMIN_PASSWORD precisam estar definidos."

    senha_ok, mensagem_senha = auth.validar_senha_forte(senha)
    if not senha_ok:
        return False, f"Senha do administrador fraca: {mensagem_senha}"

    existente = db.buscar_usuario_por_nome(nome_usuario)
    senha_hash, salt = auth.gerar_hash_senha(senha)

    if existente:
        db.atualizar_senha_usuario(existente["id"], senha_hash, salt)
        db.definir_tipo_usuario(existente["id"], TIPO_ADMIN)
        if not existente["email_confirmado"]:
            db.confirmar_email_usuario(existente["id"])
        return True, f"Administrador '{nome_usuario}' atualizado."

    try:
        db.criar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            nome_completo="Administrador",
            senha_hash=senha_hash,
            salt=salt,
            tipo=TIPO_ADMIN,
            token_confirmacao=None,
            data_criacao=datetime.now().isoformat(timespec="seconds"),
            email_confirmado=True,
        )
    except sqlite3.IntegrityError:
        return False, "JÃ¡ existe uma conta com esse nome de usuÃ¡rio ou e-mail."

    return True, f"Administrador '{nome_usuario}' criado com sucesso."


def garantir_admin_via_env():
    """Garante que sempre exista um administrador.

    Prioridade:
    1. ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD (variÃ¡veis de
       ambiente), se estiverem definidas â€” use isso em produÃ§Ã£o.
    2. Caso contrÃ¡rio, cria a conta padrÃ£o (admin / Admin@123), para
       o projeto jÃ¡ sair funcionando sem nenhuma configuraÃ§Ã£o extra.

    SÃ³ roda se ainda nÃ£o existir nenhum administrador no banco â€” nÃ£o
    fica recriando/sobrescrevendo a cada execuÃ§Ã£o do app.
    """

    if db.contar_usuarios() and any(
        u["tipo"] == TIPO_ADMIN for u in db.listar_usuarios()
    ):
        return  # jÃ¡ existe um administrador, nÃ£o faz nada

    nome_usuario = os.environ.get("ADMIN_USERNAME") or ADMIN_USUARIO_PADRAO
    email = os.environ.get("ADMIN_EMAIL") or ADMIN_EMAIL_PADRAO
    senha = os.environ.get("ADMIN_PASSWORD") or ADMIN_SENHA_PADRAO

    criar_ou_atualizar_admin(nome_usuario, email, senha)


def listar_usuarios_admin():
    """Lista de usuÃ¡rios para o painel de administraÃ§Ã£o."""
    return db.listar_usuarios()


def alterar_tipo_usuario_admin(usuario_id, novo_tipo):
    db.definir_tipo_usuario(usuario_id, novo_tipo)


def confirmar_email_manualmente_admin(usuario_id):
    db.confirmar_email_usuario(usuario_id)


def excluir_usuario_admin(usuario_id):
    db.excluir_usuario(usuario_id)


def desativar_usuario_admin(usuario_id):
    db.definir_ativo_usuario(usuario_id, False)


def ativar_usuario_admin(usuario_id):
    db.definir_ativo_usuario(usuario_id, True)


# ==========================================
# INICIALIZAÃ‡ÃƒO
# ==========================================

def _semear_usuarios_demo():
    """Cria as contas de demonstraÃ§Ã£o (equivalentes Ã s que existiam
    como dicionÃ¡rio fixo antes) jÃ¡ com senha em hash e e-mail
    confirmado, para o app continuar utilizÃ¡vel de imediato."""

    demo = [
        ("marcos", "marcos@example.com", "Marcos Silva", "Marcos@123", TIPO_LOCATARIO),
        ("fernanda", "fernanda@example.com", "Fernanda Reis", "Fernanda@123", TIPO_LOCATARIO),
        ("ana", "ana@example.com", "Ana Souza", "Ana@12345", TIPO_PROPRIETARIO),
    ]

    for nome_usuario, email, nome_completo, senha, tipo in demo:
        senha_hash, salt = auth.gerar_hash_senha(senha)
        db.criar_usuario(
            nome_usuario=nome_usuario,
            email=email,
            nome_completo=nome_completo,
            senha_hash=senha_hash,
            salt=salt,
            tipo=tipo,
            token_confirmacao=None,
            data_criacao=datetime.now().isoformat(timespec="seconds"),
            email_confirmado=True,
        )


def inicializar_estado():
    """Roda uma Ãºnica vez por sessÃ£o. Cria a fonte Ãºnica de
    verdade dos dados do app (usuÃ¡rios, salas e reservas)."""
    if "inicializado" in st.session_state:
        return

    st.session_state.inicializado = True
    st.session_state.usuario = None  # None = ninguÃ©m logado ainda
    st.session_state.donos_salas = {}

    db.criar_tabelas()

    if db.contar_salas() == 0:
        db.cadastrar_sala(
            nome="Sala Executiva", capacidade=12, localizacao="2Âº andar",
            projetor=True, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de ReuniÃ£o 01", capacidade=8, localizacao="2Âº andar",
            projetor=False, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de ReuniÃ£o 02", capacidade=8, localizacao="2Âº andar",
            projetor=False, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )
        db.cadastrar_sala(
            nome="Sala de Treinamento", capacidade=20, localizacao="3Âº andar",
            projetor=True, computador=False, internet=True,
            webcam=False, quadro=False, ar_condicionado=False
        )

    if db.contar_usuarios() == 0:
        _semear_usuarios_demo()

    garantir_admin_via_env()

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

