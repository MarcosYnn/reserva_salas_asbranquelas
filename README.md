[README.md](https://github.com/user-attachments/files/34821517/README.md)
# Sistema de Reserva de Salas

Projeto acadêmico da equipe **As Branquelas**, desenvolvido na disciplina de **Programação Web**, para consultar espaços, acompanhar reservas e gerenciar salas e contas.

> **2ª etapa — documentação revisada em 13/11/2026:** a autenticação utiliza Firebase Authentication, e usuários e salas são armazenados no Cloud Firestore. As reservas e os favoritos ainda ficam na sessão do Streamlit. Esta documentação descreve o código da `main` após o [PR #7](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/7), na base [bdab79c](https://github.com/MarcosYnn/reserva_salas_asbranquelas/commit/bdab79c116145d20d05cb9ee54897403997fc4f8). Não comprova a configuração nem o funcionamento do ambiente publicado.

## Problema

O gerenciamento manual de espaços dificulta a consulta de capacidade, localização, recursos e horários. A proposta busca centralizar essas informações e reduzir conflitos e duplicidades de reservas. A prevenção completa de conflitos ainda é uma pendência da implementação.

## Público-alvo

Alunos, professores, funcionários, coordenadores e colaboradores que utilizam espaços de uma instituição.

| Perfil | Finalidade |
| --- | --- |
| Locatário | Consultar salas e acompanhar suas reservas |
| Proprietário | Cadastrar salas e acompanhar a utilização dos seus espaços |
| Administrador | Gerenciar contas e acessar as páginas de proprietário disponíveis no menu |

## Proposta de solução

Desenvolver uma aplicação web que reúna consulta de salas, filtros, reservas, favoritos, informações de perfil e administração de contas. Manutenção, calendário, filtros completos e persistência das reservas fazem parte da evolução prevista.

## Objetivo do MVP

Demonstrar o fluxo de acesso, consulta e reserva de salas em uma interface navegável. Na versão atual, as contas são cadastradas por um administrador; não há cadastro público na tela de login.

Fluxo disponível: **login → dashboard → buscar salas → reservar → minhas reservas**.

Esse fluxo ainda possui limitações de validação, persistência e isolamento entre usuários. Ter uma reserva visível na sessão não significa que ela esteja salva ou que outros usuários tenham o mesmo horário bloqueado.

## Funcionalidades e situação atual

**Implementado** indica código acessível pela interface, sujeito a validação no ambiente configurado. **Parcial** indica comportamento incompleto. **Pendente** indica ausência do fluxo completo.

| Área | Situação | O que existe e quais são os limites |
| --- | --- | --- |
| Login e logout | Implementado | Login com nome de usuário e senha via Firebase; logout encerra o usuário da sessão |
| Cadastro de contas | Implementado | Administrador cadastra usuário, nome, e-mail, senha inicial, perfil e status |
| Administração de contas | Implementado | Listagem, edição, troca de senha, alteração de perfil/status e exclusão com confirmação; controles contra alteração da própria conta e remoção do último administrador ativo |
| Perfis e navegação | Parcial | Menus e verificações por perfil; mudanças de permissão ou bloqueio de uma conta já conectada precisam de validação |
| Salas | Parcial | Cadastro com capacidade, localização e recursos no Firestore; listagem de salas do proprietário; edição e indisponibilidade ainda pendentes |
| Busca | Parcial | Data, horário inicial/final e capacidade; compara horários por igualdade e não resolve sobreposições |
| Reservas | Parcial | Inclusão e listagem em `st.session_state`, inicialmente com exemplos de demonstração; sem persistência compartilhada |
| Cancelamento | Parcial | Componente possui botão opcional, mas a página “Minhas Reservas” não habilita essa opção |
| Favoritos | Parcial | Inclusão/remoção na sessão; não persistem por conta e o botão de reserva pode reutilizar dados antigos da busca |
| Dashboard | Parcial | Contagens calculadas a partir da sessão, com datas fixas e indicadores demonstrativos |
| Perfil | Parcial | Consulta de dados; não há formulário para o usuário editar seu próprio perfil |
| Cadastro público, confirmação e recuperação de senha | Pendente no fluxo atual | Não estão expostos na tela de login; funções antigas de SMTP/hash continuam no código, mas não representam integração desses fluxos |
| Manutenção, avisos de indisponibilidade e acessibilidade das salas | Pendente | Requisitos previstos, sem fluxo completo |
| Calendário visual | Pendente | Não há página ou opção no menu; este README não registra o card como implementado |
| Responsividade | A validar | Interface e CSS existentes; validação em celular e diferentes tamanhos de tela ainda deve ser evidenciada |

## Levantamento de requisitos

Os identificadores abaixo preservam o levantamento anterior para manter a rastreabilidade dos cards. São **requisitos e critérios desejados**, não uma declaração de que todos estejam atendidos. O estado da implementação está na tabela acima e nas pendências da revisão.

## Requisitos funcionais

| Código | Requisito | Situação no código |
| --- | --- | --- |
| RF01 | O sistema deve permitir o cadastro de usuários. | Cadastro pelo administrador |
| RF02 | O sistema deve permitir que o usuário realize login utilizando suas credenciais. | Implementado |
| RF03 | O sistema deve apresentar um Dashboard após o acesso do usuário. | Parcial: indicadores demonstrativos |
| RF04 | O sistema deve permitir consultar as salas cadastradas. | Implementado |
| RF05 | O sistema deve apresentar informações sobre cada sala, como nome, capacidade, localização e recursos disponíveis. | Implementado |
| RF06 | O sistema deve informar a situação atual de cada sala. | Pendente |
| RF07 | O sistema deve permitir consultar a disponibilidade de uma sala. | Parcial: conflitos incompletos |
| RF08 | O sistema deve permitir selecionar uma sala para reserva. | Implementado na sessão |
| RF09 | O sistema deve permitir selecionar a data da reserva. | Implementado na busca |
| RF10 | O sistema deve permitir selecionar o horário inicial e final da reserva. | Parcial: falta validar período |
| RF11 | O sistema deve permitir informar a finalidade da reserva quando necessário. | Pendente |
| RF12 | O sistema deve permitir confirmar uma reserva. | Parcial: sem revalidar disponibilidade |
| RF13 | O sistema deve registrar as reservas realizadas. | Parcial: somente sessão |
| RF14 | O sistema deve permitir que o usuário consulte suas reservas. | Parcial: filtro por nome |
| RF15 | O sistema deve apresentar sala, data, horário e status das reservas realizadas. | Implementado na sessão |
| RF16 | O sistema deve permitir cancelar uma reserva quando permitido. | Parcial: botão não habilitado na página |
| RF17 | O sistema deve liberar novamente o horário após o cancelamento de uma reserva. | Pendente no fluxo de cancelamento |
| RF18 | O sistema deve impedir reservas conflitantes para uma mesma sala e período. | Pendente: sobreposições permitidas |
| RF19 | O sistema deve permitir buscar salas por características, como capacidade, localização e recursos disponíveis. | Parcial: somente capacidade e período |
| RF20 | O sistema deve permitir utilizar filtros para facilitar a localização de salas. | Parcial |
| RF21 | O sistema deve permitir filtrar salas pela quantidade de pessoas. | Implementado |
| RF22 | O sistema deve permitir identificar equipamentos e recursos existentes em cada sala. | Implementado |
| RF23 | O sistema deve apresentar avisos sobre salas temporariamente indisponíveis. | Pendente |
| RF24 | O sistema deve apresentar avisos sobre salas que estejam em manutenção. | Pendente |
| RF25 | O sistema deve possuir uma área administrativa destinada a usuários autorizados. | Implementado |
| RF26 | O sistema deve permitir o cadastro de salas. | Implementado |
| RF27 | O sistema deve permitir a atualização das informações das salas. | Pendente |
| RF28 | O sistema deve permitir alterar a disponibilidade das salas. | Pendente |
| RF29 | O sistema deve permitir informar períodos de manutenção. | Pendente |
| RF30 | O administrador deve poder consultar informações do sistema. | Parcial: contas e páginas de proprietário |
| RF31 | O sistema deve apresentar informações claras sobre os recursos disponíveis em cada sala. | Implementado |
| RF32 | O sistema deve utilizar indicadores visuais para representar características das salas. | Parcial |
| RF33 | O sistema deve apresentar informações relacionadas aos recursos de acessibilidade disponíveis. | Pendente |
| RF34 | O usuário deve poder favoritar salas. | Implementado na sessão |
| RF35 | O sistema deve permitir recuperação e redefinição de senha. | Pendente no fluxo atual |
| RF36 | O administrador deve poder gerenciar as contas cadastradas. | Implementado |
| RF37 | O administrador deve poder bloquear e reativar contas. | Implementado; sessões ativas a validar |
| RF38 | O administrador deve poder alterar o tipo de conta de um usuário. | Implementado; sessões ativas a validar |


## Requisitos não funcionais

| Código | Requisito |
| ------ | -------------------------------------------------------------------------------------------------------------- |
| RNF01 | A interface deve ser simples, clara e intuitiva. |
| RNF02 | A navegação deve manter uma identidade visual consistente. |
| RNF03 | A aplicação deve possuir interface responsiva. |
| RNF04 | O sistema deve funcionar adequadamente em diferentes tamanhos de tela. |
| RNF05 | As principais funcionalidades devem permanecer acessíveis em dispositivos móveis. |
| RNF06 | As informações devem estar organizadas para que o usuário localize rapidamente as funcionalidades necessárias. |
| RNF07 | O sistema deve apresentar mensagens claras durante as operações. |
| RNF08 | Os botões e elementos interativos devem apresentar respostas visuais às ações do usuário. |
| RNF09 | A interface deve informar claramente quando uma operação for concluída ou apresentar erro. |
| RNF10 | O acesso às funcionalidades administrativas deve ser restrito a usuários autorizados. |
| RNF11 | O sistema deve evitar conflitos e duplicidades de reservas. |
| RNF12 | A interface deve utilizar elementos visuais consistentes, como cores, ícones, botões, cards e formulários. |
| RNF13 | As informações sobre disponibilidade e indisponibilidade devem ser apresentadas de maneira clara. |
| RNF14 | Os elementos da interface devem possuir tamanho, organização e espaçamento adequados. |
| RNF15 | O projeto deve utilizar Git e GitHub para controle de versão e colaboração. |
| RNF16 | As funcionalidades desenvolvidas devem seguir os requisitos e o design definidos pela equipe. |
| RNF17 | As senhas não devem ser armazenadas em texto puro. |
| RNF18 | Credenciais externas e configurações sensíveis devem ser armazenadas por meio de variáveis de ambiente. |


## Regras de negócio

| Código | Regra |
| ------ | ------------------------------------------------------------------------------------------------------ |
| RN01 | Somente usuários cadastrados podem realizar login. |
| RN02 | O usuário deve estar autenticado para acessar as funcionalidades internas do sistema. |
| RN03 | Toda reserva deve estar associada a uma sala. |
| RN04 | Toda reserva deve possuir uma data definida. |
| RN05 | Toda reserva deve possuir horário inicial e horário final. |
| RN06 | O horário final deve ser posterior ao horário inicial. |
| RN07 | Uma sala não pode possuir duas reservas em períodos conflitantes. |
| RN08 | Uma reserva somente pode ser confirmada quando a sala estiver disponível no período escolhido. |
| RN09 | O usuário deve consultar a disponibilidade antes da confirmação da reserva. |
| RN10 | Quando uma reserva for cancelada, o horário correspondente deve voltar a ficar disponível. |
| RN11 | Salas em manutenção devem ser apresentadas como indisponíveis para reserva. |
| RN12 | Salas marcadas como indisponíveis não podem receber novas reservas no período informado. |
| RN13 | Apenas usuários autorizados podem acessar a área administrativa. |
| RN14 | Usuários autorizados poderão cadastrar e atualizar informações relacionadas às salas. |
| RN15 | O sistema deve manter as informações de disponibilidade atualizadas após cada reserva ou cancelamento. |
| RN16 | O usuário deve visualizar as características da sala antes de concluir uma reserva. |
| RN17 | O nome de usuário e o e-mail não podem ser duplicados. |
| RN18 | A conta precisa estar ativa para permitir o login. |
| RN19 | O usuário deverá confirmar o e-mail antes de acessar a conta quando a confirmação estiver habilitada. |
| RN20 | Cada tipo de conta deve visualizar apenas as funcionalidades permitidas para seu perfil. |


## Histórias de usuário

### HU01 — Cadastro

Como usuário, quero criar uma conta para acessar as funcionalidades privadas da plataforma.

### HU02 — Login

Como usuário, quero acessar o sistema utilizando minhas credenciais para utilizar suas funcionalidades.

### HU03 — Consulta de salas

Como usuário, quero visualizar as salas cadastradas para escolher o espaço mais adequado.

### HU04 — Busca por características

Como usuário, quero pesquisar salas por capacidade, localização e recursos para encontrar rapidamente uma opção adequada.

### HU05 — Filtros de busca

Como usuário, quero utilizar filtros para visualizar apenas as salas que atendem às minhas necessidades.

### HU06 — Recursos da sala

Como usuário, quero visualizar os recursos existentes em cada sala para saber se o ambiente é adequado à atividade que pretendo realizar.

### HU07 — Consulta de disponibilidade

Como usuário, quero consultar os horários disponíveis de uma sala para saber quando ela poderá ser utilizada.

### HU08 — Reserva de sala

Como usuário, quero selecionar uma sala, uma data e um horário para realizar uma reserva.

### HU09 — Acompanhamento

Como usuário, quero visualizar minhas reservas para acompanhar os espaços e horários reservados.

### HU10 — Cancelamento

Como usuário, quero cancelar uma reserva quando não precisar mais utilizar a sala.

### HU11 — Favoritos

Como usuário, quero favoritar salas que utilizo com frequência para encontrá-las com maior facilidade.

### HU12 — Avisos

Como usuário, quero visualizar avisos sobre salas indisponíveis ou em manutenção.

### HU13 — Acessibilidade

Como usuário, quero visualizar informações sobre recursos de acessibilidade para saber se o espaço atende às minhas necessidades.

### HU14 — Gerenciamento de salas

Como Proprietário, quero cadastrar e visualizar minhas salas para acompanhar os espaços disponibilizados.

### HU15 — Administração

Como Administrador, quero gerenciar as contas cadastradas para controlar o acesso à plataforma.

### HU16 — Recuperação de senha

Como usuário, quero recuperar minha senha por meio do meu e-mail para voltar a acessar minha conta.


## Critérios gerais de aceitação

* Os campos obrigatórios devem ser validados;
* Dados inválidos devem apresentar mensagens claras;
* Usuários sem autenticação não devem acessar áreas internas;
* O usuário deve conseguir visualizar as salas cadastradas;
* Cada sala deve apresentar suas principais características;
* O sistema deve permitir pesquisar e filtrar salas;
* Os filtros devem alterar os resultados de acordo com os critérios informados;
* O sistema deve informar quando uma sala estiver disponível;
* O sistema deve informar quando uma sala estiver indisponível;
* O usuário deve conseguir consultar a disponibilidade antes de reservar;
* O sistema não deve permitir reservas conflitantes;
* Uma reserva confirmada deve aparecer na área de reservas;
* O cancelamento deve atualizar a situação da reserva;
* Após o cancelamento, o horário deve voltar a ficar disponível;
* A área administrativa deve ser acessível somente por usuários autorizados;
* Mensagens de erro e sucesso devem ser apresentadas de forma clara;
* O sistema deve diferenciar permissões de Locatários, Proprietários e Administradores;
* Usuários bloqueados não devem conseguir acessar o sistema;
* O sistema deve impedir a duplicidade de e-mails e nomes de usuário;
* As senhas cadastradas devem atender aos critérios mínimos de segurança.



## Tecnologias utilizadas

| Tecnologia | Utilização |
| --- | --- |
| Python e Streamlit | Lógica da aplicação, interface, navegação e estado da sessão |
| Firebase Authentication | Contas, autenticação e armazenamento das credenciais |
| Cloud Firestore | Persistência de usuários e salas |
| Firebase Admin SDK | Operações de contas e acesso ao Firestore pelo servidor |
| Requests | Chamada ao endpoint de login do Firebase |
| Python-dotenv | Carregamento opcional de variáveis; não substitui os secrets exigidos pelo Firebase |
| CSS e HTML | Estilização e componentes visuais |
| Git e GitHub | Versionamento, revisão e integração |
| PraxiLab | Kanban, responsáveis, evidências e entrega acadêmica |

SQLite foi removido do fluxo atual no PR #7. As funções de hash PBKDF2 e SMTP em `controllers/auth_controller.py` são remanescentes; o login atual utiliza Firebase Authentication. Não há modo offline funcional sem configuração do Firebase.

As dependências de `requirements.txt` ainda não têm versões fixadas. Não há versão mínima de Python nem matriz de compatibilidade validada documentada no repositório.

## Arquitetura do projeto

A organização é inspirada em MVC, com parte das páginas ainda concentrada em `main.py`.

| Caminho | Responsabilidade atual |
| --- | --- |
| `app.py` | Configuração, inicialização, verificação de sessão e menu |
| `main.py` | Páginas de locatário, proprietário e administrador |
| `controllers/firebase_auth_controller.py` | Login no Firebase e verificação do token |
| `controllers/usuario_firebase_controller.py` | Validação e autorização das operações administrativas |
| `controllers/autorizacao_controller.py` | Restrições por perfil nas páginas |
| `controllers/auth_controller.py` | Validações reutilizadas e funções legadas de hash/SMTP |
| `models/firebase_client.py` | Inicialização do Admin SDK a partir dos secrets |
| `models/usuario_firebase_model.py` | Contas Auth e documentos da coleção `usuarios` |
| `models/sala_firebase_model.py` | Cadastro, listagem, exclusão e dados demonstrativos de salas |
| `utils/estado.py` | Adaptação dos dados, sessão, reservas e favoritos |
| `utils/componentes.py` | CSS, cards, listas e ações da interface |
| `views/login_view.py` | Tela de login |
| `views/admin_view.py` | Formulários administrativos de usuários |
| `assets/` | Imagens utilizadas pela interface |

`views/locatario_view.py` e `views/proprietario_view.py` estão vazios. Não há `models/database.py` nem script de criação de administrador no estado atual. A existência de pastas não significa que todas as responsabilidades já estejam separadas.

## Banco de dados e armazenamento

| Informação | Onde fica | Campos e limites |
| --- | --- | --- |
| Credenciais | Firebase Authentication | UID, e-mail, senha e situação da conta; senha não é gravada no documento do Firestore |
| Perfis | `usuarios/{uid}` no Firestore | `usuario`, `nome`, `email`, `perfil`, `status`; ID do documento deve corresponder ao UID Auth |
| Salas | `salas/{id}` no Firestore | `id`, `nome`, `capacidade`, `localizacao`, `proprietario` e flags de recursos |
| Reservas | `st.session_state.reservas` | `sala_id`, `cliente`, `data`, `horario`, `status`; sem coleção persistente |
| Favoritos | `st.session_state.favoritos` | Conjunto de IDs de salas da sessão, sem persistência por conta |

As salas permitem projetor, computador, internet, webcam, quadro e ar-condicionado. Novas salas recebem ID gerado por UUID; as demonstrativas usam IDs numéricos.

A inicialização grava quatro salas de demonstração se a coleção `salas` estiver vazia. Também recria reservas demonstrativas na sessão para as salas cujos IDs forem encontrados. Esses dados não são agendamentos reais.

Reservas são relacionadas ao nome do cliente, e salas ao login do proprietário. A evolução deve adotar identificadores estáveis, evitando mistura de contas com nomes iguais e perda do vínculo quando o login for alterado.

Não há migração automática de contas ou salas de antigos bancos SQLite. Os dados já existentes no projeto Firebase precisam ser conferidos antes de qualquer alteração.

## Autenticação, perfis e permissões

O login recebe **nome de usuário e senha**. O servidor procura o perfil no Firestore, obtém o e-mail associado, solicita autenticação ao Firebase e verifica o token retornado.

- Usuário: de 3 a 30 caracteres, normalizado em minúsculas, com letras sem acento, números, ponto, hífen ou sublinhado.
- Senha nos formulários administrativos: pelo menos oito caracteres, com maiúscula, minúscula e número.
- Perfis aceitos: `Locatário`, `Proprietário` e `Administrador`.
- Status aceitos: `ativo` e `inativo`.

Para perfis antigos sem `usuario`, o modelo usa temporariamente a parte do e-mail anterior ao `@`. Se houver mais de um perfil com o mesmo login, a busca não escolhe um deles. O administrador deve revisar esses perfis e cadastrar logins explícitos e distintos.

| Perfil | Páginas disponíveis |
| --- | --- |
| Locatário | Dashboard, Buscar Salas, Minhas Reservas, Favoritos e Perfil |
| Proprietário | Dashboard, Minhas Salas e Perfil |
| Administrador | Páginas de proprietário e Administração de usuários |

O menu administrativo reutiliza as páginas de proprietário, que filtram salas pelo login. Portanto, “administrador” ainda não equivale a uma tela completa de gestão de todas as salas.

As operações administrativas verificam o perfil recebido, bloqueiam alteração/exclusão da própria conta e buscam preservar o último administrador ativo. Ainda é necessário validar concorrência, vínculo entre UID do perfil e UID autenticado e atualização das permissões de sessões já abertas. O uso do Admin SDK exige que as verificações de autorização sejam mantidas no servidor.

A tela atual não oferece cadastro público, confirmação de e-mail nem recuperação de senha pelo usuário. O administrador pode definir uma nova senha pelo painel; isso não é um fluxo de recuperação por e-mail.

## Como executar o projeto

### Pré-requisitos

- Python e Git instalados.
- Um projeto Firebase destinado aos testes, com Authentication e Cloud Firestore configurados.
- Provedor **E-mail/senha** habilitado no Firebase Authentication.
- Conta de serviço autorizada para as operações utilizadas pelo servidor.
- Conta administrativa inicial configurada conforme a seção seguinte.

### Preparar o ambiente

~~~bash
git clone https://github.com/MarcosYnn/reserva_salas_asbranquelas.git
cd reserva_salas_asbranquelas
~~~

No Windows/PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

No Linux/macOS:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
~~~

### Configurar Firebase e Streamlit

Crie localmente `.streamlit/secrets.toml` com a estrutura abaixo. Os valores são exemplos: substitua `service_account_json` pelo JSON completo da conta de serviço, preservando os escapes `\n` da chave privada.

~~~toml
[firebase]
project_id = "SEU_PROJECT_ID"
web_api_key = "SUA_WEB_API_KEY"
service_account_json = '''
{
  "type": "service_account",
  "project_id": "SEU_PROJECT_ID",
  "private_key_id": "SUBSTITUIR",
  "private_key": "SUBSTITUIR_PELO_VALOR_DO_JSON",
  "client_email": "SUBSTITUIR",
  "client_id": "SUBSTITUIR",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
'''
~~~

`project_id`, a conta de serviço e a Web API Key devem pertencer ao mesmo projeto. O cliente verifica a igualdade entre o Project ID configurado e o JSON da conta de serviço.

No Streamlit Community Cloud, configure o mesmo conteúdo no campo de secrets da aplicação. O arquivo real está no `.gitignore` e não deve ser anexado a cards, commits, capturas ou relatórios.

O repositório não fornece `.env.example` nem `secrets.toml` preenchido. Variáveis SMTP do código antigo não são necessárias para o login Firebase atual.

### Preparar o primeiro administrador

Não existe criação automática de administrador nem senha padrão no código atual.

Um responsável com acesso autorizado ao projeto Firebase deve:

1. Criar uma conta de teste no Firebase Authentication com e-mail e senha.
2. Copiar seu UID.
3. Criar no Firestore um documento em `usuarios` com **esse mesmo UID** como ID.
4. Preencher os campos abaixo, usando o mesmo e-mail da conta Auth.

~~~json
{
  "usuario": "admin_teste",
  "nome": "Administrador de Teste",
  "email": "EMAIL_DA_CONTA_AUTH",
  "perfil": "Administrador",
  "status": "ativo"
}
~~~

Depois, entre com o login configurado em `usuario` e a senha da conta Auth. As demais contas podem ser cadastradas no painel administrativo. Não basta criar somente o usuário Auth ou somente o documento do Firestore.

### Iniciar a aplicação

~~~bash
python -m streamlit run app.py
~~~

Acesse o endereço exibido no terminal, normalmente `http://localhost:8501`.

| Problema | Verificação inicial |
| --- | --- |
| Secrets não encontrados | Conferir caminho local ou configuração de secrets no Streamlit Cloud |
| Project ID divergente | Conferir o projeto informado e o JSON da conta de serviço |
| Login recusado | Conferir login, e-mail correspondente no Auth, senha, status e perfil |
| Perfil antigo não localizado | Revisar o campo `usuario` e possíveis logins repetidos |
| Erro de acesso ao Firestore | Conferir credenciais e permissões do projeto de teste |
| Salas de exemplo inesperadas | A inicialização preenche a coleção quando ela está vazia |

## Revisão do código — 13/11/2026

A análise considera o código da base indicada no início deste README. Os problemas abaixo são pendências de implementação ou validação; documentá-los não significa corrigi-los.

| ID | Prioridade | Constatação e encaminhamento |
| --- | --- | --- |
| REV01 | Alta | Persistir reservas e favoritos, vinculando-os ao UID da conta e ao ID da sala |
| REV02 | Alta | A busca compara a string completa do horário; implementar sobreposição de intervalos e proteção contra duas confirmações simultâneas |
| REV03 | Alta | O botão Reservar apenas adiciona à lista; revalidar disponibilidade, datas e horários e impedir duplicação |
| REV04 | Alta | Favoritos permite reservar com dados ausentes ou antigos; exigir seleção explícita de período |
| REV05 | Alta | Filtragem de reservas por nome e vínculo de salas por login; substituir por identificadores estáveis |
| REV06 | Alta | Conferir UID do perfil com UID autenticado e revalidar status/permissões em sessões já abertas |
| REV07 | Média | `render_lista_reservas()` captura `StopIteration`, mas `sala_por_id()` lança `ValueError`; tratar sala ausente |
| REV08 | Média | Cancelamento não está habilitado na página; concluir fluxo autorizado e liberar disponibilidade |
| REV09 | Média | Substituir datas fixas e escolher a próxima reserva pela data/horário; faturamento e gráfico do proprietário são demonstrativos |
| REV10 | Média | Completar manutenção, filtros de recursos/localização, calendário e edição de salas/perfil |
| REV11 | Média | Validar responsividade, mensagens e erros; fixar versões de dependências e estabelecer testes reproduzíveis |

A revisão do card **“Revisão do código”** deve vincular cada correção ao card correspondente do PraxiLab e ao PR que a implementar. O calendário é uma funcionalidade separada e continua pendente.

## Testes e validação

Esta atualização documental foi baseada na leitura do código e do histórico de integração. **Não registra uma execução de ponta a ponta da aplicação publicada nem aprovação dos testes abaixo.** O repositório da base revisada não contém suíte automatizada de testes nem workflow de CI.

Utilizar contas e projeto Firebase de teste. Os casos de regressão associados às pendências devem ser repetidos após as correções.

| Caso | Procedimento e resultado esperado | Situação |
| --- | --- | --- |
| T01 | Acessar sem login: conteúdo interno e menu protegidos | A executar |
| T02 | Entrar com cada perfil e verificar somente as páginas permitidas | A executar |
| T03 | Tentar senha incorreta, conta inativa e perfil inválido: acesso recusado | A executar |
| T04 | Administrador criar, editar e excluir conta de teste; conferir Auth e Firestore | A executar |
| T05 | Tentar alterar a própria conta e remover o último admin ativo: operação recusada | A executar |
| T06 | Cadastrar sala, abrir nova sessão e conferir persistência e vínculo do proprietário | A executar |
| T07 | Reservar e abrir outra sessão: mesma reserva e bloqueio devem estar disponíveis | Bloqueado por REV01 |
| T08 | Reservar 9h–11h e tentar 10h–12h, repetir clique e disputar horário em duas sessões | Regressão de REV02/REV03 |
| T09 | Tentar término anterior/igual ao início e data passada: impedir reserva | Regressão de REV03 |
| T10 | Reservar a partir de Favoritos sem busca anterior: exigir período válido | Regressão de REV04 |
| T11 | Cancelar a própria reserva e consultar novamente a disponibilidade | Depende de REV08 e persistência |
| T12 | Usar contas de nomes iguais e alternar login/logout: dados devem ficar isolados | Regressão de REV01/REV05 |
| T13 | Exibir reserva de sala removida: tratar ausência sem interromper a página | Regressão de REV07 |
| T14 | Bloquear ou alterar perfil de conta já conectada e verificar restrição de acesso | Regressão de REV06 |
| T15 | Conferir layout, contraste e operações em computador e celular | A executar |

Cada execução deve registrar data, responsável, ambiente, passos, resultado observado, evidência e eventual card de erro. Não marcar teste como aprovado apenas porque existe código para a funcionalidade.

## Organização do projeto e critérios da 2ª etapa

A equipe utiliza o Kanban do PraxiLab: **Backlog → A Fazer → Em Andamento → Revisão → Concluído**.

Conforme a orientação do professor:

- Cada integrante deve criar ou assumir suas próprias tarefas, atualizar seu andamento e evidenciar autonomia.
- Todos devem contribuir efetivamente com codificação em branch própria e ter **pelo menos 10 commits relevantes por integrante na etapa**.
- Toda contribuição no código deve estar vinculada a um card do PraxiLab.
- O líder realiza a entrega final na plataforma com o relatório do projeto e das contribuições de cada integrante.
- A avaliação é individual e considera as evidências reais de participação.

O professor também informou que a remoção por falta de participação depende de avaliação docente, impede ingresso em outra equipe nesta etapa e pode resultar em reprovação conforme os critérios da disciplina.

### Fluxo de contribuição

1. Registrar no card objetivo, responsável, prioridade, prazo, critérios de aceitação e dependências.
2. Atualizar a base e criar branch própria, como `feature/arthur-reservas` ou `docs/arthur-readme`.
3. Desenvolver e produzir commits que representem mudanças relevantes.
4. Referenciar o identificador real do card nas mensagens e no PR. Não inventar IDs.
5. Testar o comportamento alterado e registrar o resultado.
6. Atualizar a documentação afetada na própria PR; cada integrante documenta sua alteração.
7. Abrir PR, solicitar revisão de outro integrante e anexar os links ao card.
8. Mover para Concluído após revisão, integração e registro das evidências.

Revisões e documentação são contribuições úteis, mas não substituem a exigência de codificação. O mínimo de commits é por integrante na etapa, não por card; o total não deve ser alcançado por alterações artificiais. Este README não certifica que alguém já cumpriu a quantidade exigida.

### Registro para o relatório final

| Campo | O que registrar |
| --- | --- |
| Integrante | Nome e conta GitHub |
| Card | Identificador, título e link real no PraxiLab |
| Contribuição | Problema, implementação e resultado obtido |
| GitHub | Branch, commits, PR e integração |
| Validação | Testes executados, resultados e evidências |
| Documentação | Seções atualizadas |
| Pendências | Limites e dependências ainda não concluídos |

O card **“Revisão do código”** tem a revisão registrada nesta documentação; as correções continuam pendentes até serem implementadas e validadas. O estado do quadro PraxiLab deve ser atualizado pelos responsáveis.

## Integrantes e contribuições registradas

As responsabilidades abaixo preservam o registro anterior da equipe. As evidências específicas devem ser complementadas pelos integrantes nos cards e no relatório final; responsabilidade atribuída não comprova, por si só, autoria de todos os módulos.

| Integrante | Papel | Participação registrada |
| --- | --- | --- |
| Alexandre Amorim | Scrum Master | Organização e acompanhamento da equipe; participação registrada em autenticação, revisão, ajustes de banco e login; histórico também contém correções de caracteres, painel e usabilidade |
| Arthur Coelho | Documentação e requisitos | Organização do README, requisitos, regras e critérios; histórico de atualizações documentais; revisão das pendências e preparação desta atualização, sujeita a revisão e integração |
| Emerson Castro | Back-end | Participação registrada na estrutura MVC, dashboard, autenticação e ajustes técnicos; histórico contém alterações em `app.py`, `main.py`, estado e login |
| Giullia Di Fátima | Front-end e Design | Design e organização da interface; histórico contém ajustes de layout, textos, imagens e tela de login |
| João Carlos Neres | Levantamento de requisitos e integração Firebase | Necessidades dos usuários; histórico e PRs #6 e #7 registram CRUD de contas, integração Firebase e migração de login e salas |
| Marcos Yan | Back-end | Participação registrada em desenvolvimento, integração Streamlit/GitHub, testes de funcionalidade, estrutura MVC, dashboard e autenticação; vincular evidências específicas no relatório |
| Paulo Nathan | Design | Participação registrada na criação visual e organização das telas; vincular evidências específicas no relatório |

### Evidências disponíveis no GitHub

- [Histórico do README](https://github.com/MarcosYnn/reserva_salas_asbranquelas/commits/main/README.md): atualizações anteriores de Arthur (`Art455hur`).
- [PR #2 — Tela de cadastro](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/2): entrega histórica integrada; não comprova existência do cadastro público na interface atual.
- [PR #4 — Mudança de código na tela de cadastro](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/4): alterações históricas integradas.
- [PR #6 — Firebase e CRUD de usuários](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/6): integração já realizada.
- [PR #7 — Migração de autenticação e correções](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/7): integrado em 13/11/2026; login, perfis e salas com Firebase.
- [Histórico geral](https://github.com/MarcosYnn/reserva_salas_asbranquelas/commits/main/): consultar autoria e alterações antes de preencher o relatório.

Na base revisada, o PR #3 adicionava uma imagem e o PR #5 propunha alterações em `app.py`; ambos ainda estavam abertos. Não são contabilizados aqui como entregas integradas.

## Links do projeto

- [Repositório no GitHub](https://github.com/MarcosYnn/reserva_salas_asbranquelas)
- [Aplicação cadastrada no repositório](https://reservasalasasbranquelas-znumjlvbtfpn9kejpwh5dl.streamlit.app/)
- [Issues](https://github.com/MarcosYnn/reserva_salas_asbranquelas/issues)
- [Pull Requests](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pulls)

O link da aplicação é o endereço registrado pelo projeto; sua disponibilidade e configuração não foram verificadas nesta revisão. O repositório não informa um link público do quadro PraxiLab ou um protótipo Figma para incluir aqui.

## Próximos passos

1. Concluir persistência compartilhada e vínculo das reservas por UID.
2. Corrigir disponibilidade, sobreposições, duplicações e validação de período.
3. Completar cancelamento, isolamento entre contas e atualização de permissões.
4. Tratar sala inexistente, datas fixas e indicadores demonstrativos.
5. Implementar as funcionalidades pendentes dos cards, incluindo manutenção, filtros e calendário.
6. Executar os roteiros de teste e registrar evidências individuais.
7. Atualizar README e cards em cada PR e consolidar o relatório para a entrega final.

A prioridade é concluir o fluxo de reserva com dados consistentes entre sessões. Esta documentação acompanha o código e deve ser revisada quando novas alterações forem integradas.

