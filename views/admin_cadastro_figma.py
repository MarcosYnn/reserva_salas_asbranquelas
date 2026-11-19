import re
import streamlit as st
from controllers.usuario_firebase_controller import criar_usuario_admin
from utils.estado import TIPO_ADMIN, TIPO_LOCATARIO, TIPO_PROPRIETARIO


def renderizar_cadastro_figma(usuario):
    """Tela de cadastro inspirada no Figma; persistência via controlador Firebase existente."""
    st.markdown("""<style>
    .cadastro-top {font-size:12px;color:#7083a1;margin:12px 0 4px}
    .cadastro-titulo {font-size:23px;font-weight:750;color:#0d1c36;margin:0 0 4px}
    .cadastro-ajuda {font-size:12px;color:#7386a4;margin-bottom:20px}
    .cadastro-box {background:white;border:1px solid #dbe4f0;border-radius:10px;padding:14px 18px;margin:12px 0 6px;font-size:14px;font-weight:700;color:#172c50}
    .cadastro-info {background:#fff;border:1px solid #dbe4f0;border-radius:10px;padding:17px;color:#1d3557;font-size:13px;margin-bottom:12px}
    .cadastro-info small {color:#7386a4}
    div[data-testid="stForm"] {background:white;border:1px solid #dbe4f0;border-radius:10px;padding:15px 18px}
    div[data-testid="stForm"] label {font-size:12px!important;color:#253d64!important}
    </style>""", unsafe_allow_html=True)
    st.markdown('<div class="cadastro-top">Início / Usuários / Novo cadastro</div>', unsafe_allow_html=True)
    st.markdown('<div class="cadastro-titulo">Cadastro de Novo Usuário <span style="font-weight:400;font-size:17px">(Acesso ao Sistema)</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="cadastro-ajuda">Preencha as informações para conceder acesso seguro ao ambiente institucional.</div>', unsafe_allow_html=True)
    esquerda, direita = st.columns([3, 1.1], gap="medium")
    with esquerda:
        with st.form("cadastro_figma", clear_on_submit=False):
            st.markdown("#### 🔵 01  Informações Pessoais")
            st.caption("Foto de perfil institucional — cadastro de imagem não habilitado nesta versão")
            nome = st.text_input("Nome completo *", placeholder="Nome e sobrenome")
            a, b = st.columns(2)
            with a:
                cpf = st.text_input("CPF *", placeholder="000.000.000-00")
            with b:
                nascimento = st.date_input("Data de nascimento *", value=None, format="DD/MM/YYYY", min_value="1900-01-01", max_value="today")
            a, b = st.columns(2)
            with a:
                email = st.text_input("E-mail institucional *", placeholder="usuario@instituicao.edu.br")
            with b:
                telefone = st.text_input("Telefone *", placeholder="(69) 99999-0000")
            st.divider()
            st.markdown("#### 🔵 02  Vinculação Profissional")
            a, b, c = st.columns(3)
            with a:
                departamento = st.selectbox("Departamento / Setor *", ["Coordenação de Curso", "Secretaria", "Direção", "Tecnologia", "Outro"])
            with b:
                cargo = st.selectbox("Função / Cargo *", ["Assistente Administrativo", "Coordenador", "Professor", "Técnico", "Outro"])
            with c:
                unidade = st.selectbox("Unidade / Local de trabalho *", ["Unidade Centro", "Campus Central", "Outra unidade"])
            st.divider()
            st.markdown("#### 🔵 03  Acessos e Permissões do Sistema")
            login = st.text_input("Nome de usuário *", placeholder="nome.sobrenome")
            a, b = st.columns(2)
            with a:
                senha = st.text_input("Senha provisória *", type="password")
            with b:
                confirma = st.text_input("Confirmar senha *", type="password")
            st.caption("Perfis e permissões de acesso")
            a, b = st.columns(2)
            with a:
                gestao = st.checkbox("Gestão acadêmica")
                cadastros = st.checkbox("Cadastros")
            with b:
                relatorios = st.checkbox("Relatórios")
                configuracoes = st.checkbox("Configurações")
            perfil = st.selectbox("Perfil de acesso no sistema *", [TIPO_LOCATARIO, TIPO_PROPRIETARIO, TIPO_ADMIN], help="Este perfil determina as permissões efetivas do sistema.")
            st.caption("As opções acadêmicas acima são visuais nesta etapa; o perfil selecionado é o que controla o acesso real.")
            salvar = st.form_submit_button("💾 Salvar cadastro", type="primary", use_container_width=True)
        if salvar:
            obrigatorios = [nome.strip(), cpf.strip(), nascimento, email.strip(), telefone.strip(), login.strip(), senha, confirma]
            if not all(obrigatorios):
                st.error("Preencha todos os campos obrigatórios.")
            elif not re.fullmatch(r"\d{11}", re.sub(r"\D", "", cpf)):
                st.error("Informe um CPF com 11 dígitos.")
            elif senha != confirma:
                st.error("As senhas não coincidem.")
            else:
                try:
                    criar_usuario_admin(
                        usuario,
                        nome,
                        email,
                        senha,
                        confirma,
                        perfil,
                        status="ativo",
                        usuario=login.strip().lower(),
                        dados_adicionais={
                            "cpf": re.sub(r"\D", "", cpf),
                            "telefone": telefone.strip(),
                            "nascimento": (
                                nascimento.isoformat()
                                if hasattr(nascimento, "isoformat")
                                else str(nascimento)
                            ),
                            "departamento": departamento,
                            "cargo": cargo,
                            "unidade": unidade,
                        },
                    )
                   
                    st.success("Usuário cadastrado com sucesso no Firebase!")
                except Exception as erro:
                    st.error(f"Não foi possível cadastrar: {erro}")
    with direita:
        st.markdown('<div class="cadastro-info"><b>Status do Cadastro</b><p>🔵 Preencha o formulário</p><small>Os campos obrigatórios precisam estar completos para salvar.</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="cadastro-info"><b>Permissões atribuídas</b><p>O perfil selecionado determina o acesso ao sistema.</p><small>Gestão acadêmica · Relatórios · Cadastros · Configurações</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="cadastro-info" style="background:#203b70;color:white"><b>APOIO DA UNIDADE</b><p>Coordenação de Curso</p><small style="color:#d3e2ff">Para ajustes de permissões específicas, entre em contato com a coordenação responsável.</small></div>', unsafe_allow_html=True)
