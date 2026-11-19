import streamlit as st

from models import sala_firebase_model as sala_model
from models import usuario_firebase_model as usuario_model
from models.firebase_client import obter_app_firebase


TIPO_LOCATARIO = "Locatário"
TIPO_PROPRIETARIO = "Proprietário"
TIPO_ADMIN = "Administrador"

PROPRIETARIO_PADRAO = "ana"

MAPA_RECURSOS = [
    ("projetor", "Projetor"),
    ("computador", "Computador"),
    ("internet", "Wi-Fi"),
    ("webcam", "Webcam"),
    ("quadro", "Quadro branco"),
    ("ar_condicionado", "Ar-condicionado"),
]


def _sala_para_dict(dados):
    flags = {
        chave: bool(dados.get(chave, False))
        for chave, _ in MAPA_RECURSOS
    }
    recursos = " • ".join(
        rotulo
        for chave, rotulo in MAPA_RECURSOS
        if flags[chave]
    ) or "Sem recursos cadastrados"

    return {
        "id": dados["id"],
        "nome": dados.get("nome", ""),
        "capacidade": int(dados.get("capacidade", 0)),
        "andar": dados.get("localizacao", ""),
        "proprietario": (
            dados.get("proprietario") or PROPRIETARIO_PADRAO
        ),
        "recursos": recursos,
        **flags,
    }


def carregar_salas():
    return [
        _sala_para_dict(dados)
        for dados in sala_model.listar_salas()
    ]


def recarregar_salas():
    st.session_state.salas = carregar_salas()


def adicionar_sala(
    nome,
    capacidade,
    localizacao,
    proprietario,
    recursos_marcados,
):
    sala_model.criar_sala(
        nome=nome,
        capacidade=capacidade,
        localizacao=localizacao,
        proprietario=proprietario,
        recursos_marcados=recursos_marcados,
    )
    recarregar_salas()


def excluir_sala(sala_id):
    sala_model.excluir_sala(sala_id)
    recarregar_salas()


def sala_por_id(sala_id):
    for sala in st.session_state.salas:
        if str(sala["id"]) == str(sala_id):
            return sala
    raise ValueError(f"Sala {sala_id} não encontrada.")


def salas_de(proprietario_login):
    login = (proprietario_login or "").strip().lower()
    salas = st.session_state.get("salas", [])

    return [
        sala
        for sala in salas
        if (
            str(sala.get("proprietario", "")).strip().lower() == login
            or (
                sala.get("proprietario") == PROPRIETARIO_PADRAO
                and login.split("@", 1)[0] == PROPRIETARIO_PADRAO
            )
        )
    ]


def reservas_de(cliente_nome):
    return [
        reserva
        for reserva in st.session_state.get("reservas", [])
        if reserva.get("cliente") == cliente_nome
    ]


def reservas_das_salas(sala_ids):
    ids = {str(sala_id) for sala_id in sala_ids}
    return [
        reserva
        for reserva in st.session_state.get("reservas", [])
        if str(reserva.get("sala_id")) in ids
    ]


def usuario_logado():
    return st.session_state.get("usuario")


def fazer_login(email, senha):
    # Importação local evita import circular com o controlador Firebase.
    from controllers.firebase_auth_controller import (
        autenticar_usuario_firebase,
    )

    return autenticar_usuario_firebase(email, senha)


def fazer_logout():
    st.session_state.usuario = None


def _exigir_admin_atual():
    usuario = usuario_logado()
    if not usuario or usuario.get("tipo") != TIPO_ADMIN:
        raise PermissionError(
            "Apenas um administrador pode gerenciar usuários."
        )
    return usuario


def listar_usuarios_admin():
    usuario = _exigir_admin_atual()
    from controllers.usuario_firebase_controller import (
        listar_usuarios_admin as listar,
    )

    return listar(usuario)


def alterar_tipo_usuario_admin(uid, novo_tipo):
    usuario_atual = _exigir_admin_atual()
    usuario = usuario_model.buscar_usuario(uid)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    from controllers.usuario_firebase_controller import (
        atualizar_usuario_admin,
    )

    atualizar_usuario_admin(
        usuario_atual,
        uid,
        usuario.get("nome", ""),
        usuario.get("email", ""),
        novo_tipo,
        usuario.get("status", "ativo"),
    )


def confirmar_email_manualmente_admin(uid):
    _exigir_admin_atual()

    from firebase_admin import auth

    auth.update_user(
        uid,
        email_verified=True,
        app=obter_app_firebase(),
    )


def excluir_usuario_admin(uid):
    usuario_atual = _exigir_admin_atual()

    from controllers.usuario_firebase_controller import (
        excluir_usuario_admin as excluir,
    )

    excluir(usuario_atual, uid)


def _alterar_status_usuario_admin(uid, status):
    usuario_atual = _exigir_admin_atual()
    usuario = usuario_model.buscar_usuario(uid)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    from controllers.usuario_firebase_controller import (
        atualizar_usuario_admin,
    )

    atualizar_usuario_admin(
        usuario_atual,
        uid,
        usuario.get("nome", ""),
        usuario.get("email", ""),
        usuario.get("perfil", TIPO_LOCATARIO),
        status,
    )


def desativar_usuario_admin(uid):
    _alterar_status_usuario_admin(uid, "inativo")


def ativar_usuario_admin(uid):
    _alterar_status_usuario_admin(uid, "ativo")


def inicializar_estado():
    if st.session_state.get("inicializado_firebase"):
        return

    sala_model.garantir_salas_demonstracao()

    # Descarta uma sessão antiga que possa ter sido autenticada pelo SQL.
    st.session_state.usuario = None
    st.session_state.donos_salas = {}
    st.session_state.salas = carregar_salas()

    reservas_demo = [
        {
            "sala_id": 3,
            "cliente": "Marcos Silva",
            "data": "17/08/2026",
            "horario": "14:00 - 16:00",
            "status": "Confirmada",
        },
        {
            "sala_id": 2,
            "cliente": "Marcos Silva",
            "data": "19/08/2026",
            "horario": "09:00 - 11:00",
            "status": "Confirmada",
        },
        {
            "sala_id": 4,
            "cliente": "Marcos Silva",
            "data": "21/08/2026",
            "horario": "15:00 - 17:00",
            "status": "Pendente",
        },
        {
            "sala_id": 1,
            "cliente": "Fernanda Reis",
            "data": "18/08/2026",
            "horario": "10:00 - 12:00",
            "status": "Confirmada",
        },
        {
            "sala_id": 4,
            "cliente": "Carlos Lima",
            "data": "19/08/2026",
            "horario": "13:00 - 15:00",
            "status": "Pendente",
        },
    ]

    ids_salas = {str(sala["id"]) for sala in st.session_state.salas}
    st.session_state.reservas = [
        reserva
        for reserva in reservas_demo
        if str(reserva["sala_id"]) in ids_salas
    ]

    st.session_state.favoritos = set()
    st.session_state.resultado_busca = None
    st.session_state.inicializado_firebase = True