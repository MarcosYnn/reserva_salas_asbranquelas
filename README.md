# Sistema de Reserva de Salas

O **Sistema de Reserva de Salas** é um projeto acadêmico desenvolvido na disciplina de **Programação Web**.

A aplicação tem como objetivo facilitar o gerenciamento e a utilização dos espaços disponíveis em uma instituição, permitindo que usuários consultem salas, pesquisem ambientes de acordo com suas necessidades, verifiquem horários disponíveis e realizem reservas de maneira simples e organizada.

O sistema busca reduzir processos manuais, evitar conflitos de horários e centralizar as informações relacionadas às salas, aos usuários e às reservas.

---

## Problema

Instituições que possuem várias salas podem enfrentar dificuldades para organizar e acompanhar a utilização desses espaços.

Entre os principais problemas identificados estão:

* Dificuldade para consultar quais salas estão disponíveis;
* Falta de organização dos horários de utilização;
* Reservas duplicadas;
* Conflitos de horário;
* Dificuldade para encontrar salas com determinadas características;
* Falta de informações sobre capacidade e recursos disponíveis;
* Falta de informações sobre salas temporariamente indisponíveis;
* Dependência de processos manuais para realizar reservas;
* Dificuldade para acompanhar reservas realizadas;
* Falta de uma área centralizada para gerenciamento das salas.

Essas dificuldades podem tornar o processo de reserva demorado, confuso e sujeito a erros.

---

## Público-alvo

### Público principal

O sistema é destinado a usuários vinculados à instituição que necessitam utilizar salas para atividades acadêmicas, administrativas ou profissionais.

Entre os possíveis usuários estão:

* Alunos;
* Professores;
* Funcionários;
* Coordenadores;
* Colaboradores da instituição.

### Perfis do sistema

Atualmente, o sistema trabalha com três tipos principais de conta:

* **Locatário** — usuário que pesquisa salas e realiza reservas;
* **Proprietário** — usuário responsável pelo cadastro e acompanhamento de suas salas;
* **Administrador** — usuário com permissões administrativas para gerenciamento das contas e acesso ampliado ao sistema.

---

## Proposta de solução

Desenvolver uma aplicação web que permita ao usuário:

* Criar uma conta;
* Realizar login;
* Acessar funcionalidades de acordo com seu perfil;
* Consultar as salas cadastradas;
* Pesquisar salas por características;
* Utilizar filtros de busca;
* Visualizar capacidade, localização e recursos disponíveis;
* Consultar disponibilidade por data e horário;
* Realizar reservas;
* Acompanhar as reservas realizadas;
* Cancelar reservas quando permitido;
* Favoritar salas;
* Visualizar avisos de indisponibilidade;
* Identificar salas em manutenção;
* Consultar e atualizar informações relacionadas ao perfil;
* Utilizar o sistema em diferentes dispositivos.

O sistema também possui funcionalidades específicas destinadas aos proprietários e administradores.

---

## Objetivo do MVP

O MVP tem como objetivo entregar uma aplicação visual, navegável e funcional capaz de demonstrar os principais fluxos do Sistema de Reserva de Salas.

O fluxo principal do usuário Locatário consiste em:

```text
Cadastro / Login
        ↓
    Dashboard
        ↓
  Buscar Salas
        ↓
Selecionar Data,
Horário e Capacidade
        ↓
Visualizar Salas
   Disponíveis
        ↓
Selecionar Sala
        ↓
Confirmar Reserva
        ↓
Minhas Reservas
```

Além desse fluxo, o sistema possui experiências diferentes para **Locatários, Proprietários e Administradores**.

---

## Funcionalidades implementadas

A versão atual do projeto já possui:

* Cadastro de usuários;
* Login com usuário ou e-mail;
* Confirmação de e-mail;
* Recuperação e redefinição de senha;
* Validação de senha;
* Controle de sessão;
* Controle de acesso por tipo de usuário;
* Dashboard;
* Busca de salas;
* Filtro por data;
* Filtro por horário;
* Filtro por capacidade;
* Visualização dos recursos existentes nas salas;
* Visualização das reservas;
* Cancelamento de reservas;
* Sistema de salas favoritas;
* Perfil do usuário;
* Cadastro de salas por Proprietários;
* Visualização das próprias salas;
* Dashboard específico para Proprietários;
* Painel de Administração;
* Gerenciamento de usuários;
* Alteração do tipo de conta;
* Confirmação administrativa de e-mail;
* Bloqueio e reativação de usuários;
* Exclusão de contas;
* Armazenamento de usuários e salas em SQLite;
* Interface desenvolvida em Streamlit;
* Separação do projeto utilizando estrutura inspirada em MVC.

---

# Levantamento de Requisitos

## Requisitos funcionais

| Código | Requisito                                                                                                         |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| RF01   | O sistema deve permitir o cadastro de usuários.                                                                   |
| RF02   | O sistema deve permitir que o usuário realize login utilizando suas credenciais.                                  |
| RF03   | O sistema deve apresentar um Dashboard após o acesso do usuário.                                                  |
| RF04   | O sistema deve permitir consultar as salas cadastradas.                                                           |
| RF05   | O sistema deve apresentar informações sobre cada sala, como nome, capacidade, localização e recursos disponíveis. |
| RF06   | O sistema deve informar a situação atual de cada sala.                                                            |
| RF07   | O sistema deve permitir consultar a disponibilidade de uma sala.                                                  |
| RF08   | O sistema deve permitir selecionar uma sala para reserva.                                                         |
| RF09   | O sistema deve permitir selecionar a data da reserva.                                                             |
| RF10   | O sistema deve permitir selecionar o horário inicial e final da reserva.                                          |
| RF11   | O sistema deve permitir informar a finalidade da reserva quando necessário.                                       |
| RF12   | O sistema deve permitir confirmar uma reserva.                                                                    |
| RF13   | O sistema deve registrar as reservas realizadas.                                                                  |
| RF14   | O sistema deve permitir que o usuário consulte suas reservas.                                                     |
| RF15   | O sistema deve apresentar sala, data, horário e status das reservas realizadas.                                   |
| RF16   | O sistema deve permitir cancelar uma reserva quando permitido.                                                    |
| RF17   | O sistema deve liberar novamente o horário após o cancelamento de uma reserva.                                    |
| RF18   | O sistema deve impedir reservas conflitantes para uma mesma sala e período.                                       |
| RF19   | O sistema deve permitir buscar salas por características, como capacidade, localização e recursos disponíveis.    |
| RF20   | O sistema deve permitir utilizar filtros para facilitar a localização de salas.                                   |
| RF21   | O sistema deve permitir filtrar salas pela quantidade de pessoas.                                                 |
| RF22   | O sistema deve permitir identificar equipamentos e recursos existentes em cada sala.                              |
| RF23   | O sistema deve apresentar avisos sobre salas temporariamente indisponíveis.                                       |
| RF24   | O sistema deve apresentar avisos sobre salas que estejam em manutenção.                                           |
| RF25   | O sistema deve possuir uma área administrativa destinada a usuários autorizados.                                  |
| RF26   | O sistema deve permitir o cadastro de salas.                                                                      |
| RF27   | O sistema deve permitir a atualização das informações das salas.                                                  |
| RF28   | O sistema deve permitir alterar a disponibilidade das salas.                                                      |
| RF29   | O sistema deve permitir informar períodos de manutenção.                                                          |
| RF30   | O administrador deve poder consultar informações do sistema.                                                      |
| RF31   | O sistema deve apresentar informações claras sobre os recursos disponíveis em cada sala.                          |
| RF32   | O sistema deve utilizar indicadores visuais para representar características das salas.                           |
| RF33   | O sistema deve apresentar informações relacionadas aos recursos de acessibilidade disponíveis.                    |
| RF34   | O usuário deve poder favoritar salas.                                                                             |
| RF35   | O sistema deve permitir recuperação e redefinição de senha.                                                       |
| RF36   | O administrador deve poder gerenciar as contas cadastradas.                                                       |
| RF37   | O administrador deve poder bloquear e reativar contas.                                                            |
| RF38   | O administrador deve poder alterar o tipo de conta de um usuário.                                                 |

---

## Requisitos não funcionais

| Código | Requisito                                                                                                      |
| ------ | -------------------------------------------------------------------------------------------------------------- |
| RNF01  | A interface deve ser simples, clara e intuitiva.                                                               |
| RNF02  | A navegação deve manter uma identidade visual consistente.                                                     |
| RNF03  | A aplicação deve possuir interface responsiva.                                                                 |
| RNF04  | O sistema deve funcionar adequadamente em diferentes tamanhos de tela.                                         |
| RNF05  | As principais funcionalidades devem permanecer acessíveis em dispositivos móveis.                              |
| RNF06  | As informações devem estar organizadas para que o usuário localize rapidamente as funcionalidades necessárias. |
| RNF07  | O sistema deve apresentar mensagens claras durante as operações.                                               |
| RNF08  | Os botões e elementos interativos devem apresentar respostas visuais às ações do usuário.                      |
| RNF09  | A interface deve informar claramente quando uma operação for concluída ou apresentar erro.                     |
| RNF10  | O acesso às funcionalidades administrativas deve ser restrito a usuários autorizados.                          |
| RNF11  | O sistema deve evitar conflitos e duplicidades de reservas.                                                    |
| RNF12  | A interface deve utilizar elementos visuais consistentes, como cores, ícones, botões, cards e formulários.     |
| RNF13  | As informações sobre disponibilidade e indisponibilidade devem ser apresentadas de maneira clara.              |
| RNF14  | Os elementos da interface devem possuir tamanho, organização e espaçamento adequados.                          |
| RNF15  | O projeto deve utilizar Git e GitHub para controle de versão e colaboração.                                    |
| RNF16  | As funcionalidades desenvolvidas devem seguir os requisitos e o design definidos pela equipe.                  |
| RNF17  | As senhas não devem ser armazenadas em texto puro.                                                             |
| RNF18  | Credenciais externas e configurações sensíveis devem ser armazenadas por meio de variáveis de ambiente.        |

---

## Regras de negócio

| Código | Regra                                                                                                  |
| ------ | ------------------------------------------------------------------------------------------------------ |
| RN01   | Somente usuários cadastrados podem realizar login.                                                     |
| RN02   | O usuário deve estar autenticado para acessar as funcionalidades internas do sistema.                  |
| RN03   | Toda reserva deve estar associada a uma sala.                                                          |
| RN04   | Toda reserva deve possuir uma data definida.                                                           |
| RN05   | Toda reserva deve possuir horário inicial e horário final.                                             |
| RN06   | O horário final deve ser posterior ao horário inicial.                                                 |
| RN07   | Uma sala não pode possuir duas reservas em períodos conflitantes.                                      |
| RN08   | Uma reserva somente pode ser confirmada quando a sala estiver disponível no período escolhido.         |
| RN09   | O usuário deve consultar a disponibilidade antes da confirmação da reserva.                            |
| RN10   | Quando uma reserva for cancelada, o horário correspondente deve voltar a ficar disponível.             |
| RN11   | Salas em manutenção devem ser apresentadas como indisponíveis para reserva.                            |
| RN12   | Salas marcadas como indisponíveis não podem receber novas reservas no período informado.               |
| RN13   | Apenas usuários autorizados podem acessar a área administrativa.                                       |
| RN14   | Usuários autorizados poderão cadastrar e atualizar informações relacionadas às salas.                  |
| RN15   | O sistema deve manter as informações de disponibilidade atualizadas após cada reserva ou cancelamento. |
| RN16   | O usuário deve visualizar as características da sala antes de concluir uma reserva.                    |
| RN17   | O nome de usuário e o e-mail não podem ser duplicados.                                                 |
| RN18   | A conta precisa estar ativa para permitir o login.                                                     |
| RN19   | O usuário deverá confirmar o e-mail antes de acessar a conta quando a confirmação estiver habilitada.  |
| RN20   | Cada tipo de conta deve visualizar apenas as funcionalidades permitidas para seu perfil.               |

---

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

---

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

---

## Tecnologias utilizadas

| Tecnologia         | Utilização e justificativa                                                          |
| ------------------ | ----------------------------------------------------------------------------------- |
| Python             | Linguagem principal utilizada na lógica e desenvolvimento da aplicação.             |
| Streamlit          | Criação da interface web e componentes interativos.                                 |
| SQLite             | Persistência local das informações de usuários e salas.                             |
| Python-dotenv      | Carregamento de variáveis de ambiente e configurações externas.                     |
| Git                | Controle de versão local do projeto.                                                |
| GitHub             | Repositório compartilhado, histórico de alterações e colaboração da equipe.         |
| MVC                | Organização das responsabilidades entre interface, controle e acesso aos dados.     |
| SMTP               | Possibilidade de envio de e-mails para confirmação da conta e redefinição de senha. |
| PBKDF2-HMAC-SHA256 | Proteção das senhas cadastradas por meio de hash e salt.                            |

---

## Arquitetura inicial

O projeto utiliza uma organização inspirada no padrão **MVC — Model, View e Controller**.

```text
reserva_salas_asbranquelas/
│
├── app.py
├── main.py
├── requirements.txt
│
├── controllers/
│   ├── auth_controller.py
│   └── autorizacao_controller.py
│
├── models/
│   └── database.py
│
├── views/
│   ├── login_view.py
│   ├── locatario_view.py
│   ├── proprietario_view.py
│   └── admin_view.py
│
├── utils/
│   ├── componentes.py
│   └── estado.py
│
├── assets/
└── scripts/
```

### Responsabilidades principais

* `app.py`: configuração da aplicação, sessão, autenticação e navegação;
* `main.py`: páginas e funcionalidades relacionadas aos diferentes tipos de usuário;
* `controllers/auth_controller.py`: autenticação, validação, proteção de senhas, tokens e envio de e-mails;
* `controllers/autorizacao_controller.py`: controle de autorização e permissões;
* `models/database.py`: conexão e operações realizadas no banco SQLite;
* `views/login_view.py`: interface de login, cadastro e recuperação de senha;
* `utils/componentes.py`: elementos visuais reutilizáveis;
* `utils/estado.py`: gerenciamento do estado da aplicação e integração entre banco, sessão e regras do sistema.

---

## Banco de dados e armazenamento

O projeto utiliza **SQLite** para armazenamento local de dados.

### Salas

Entre as informações armazenadas estão:

* Nome;
* Capacidade;
* Localização;
* Projetor;
* Computador;
* Internet;
* Webcam;
* Quadro;
* Ar-condicionado.

### Usuários

São armazenadas informações como:

* Nome de usuário;
* E-mail;
* Nome completo;
* Hash da senha;
* Salt utilizado no hash;
* Tipo de conta;
* Situação da conta;
* Confirmação de e-mail;
* Token de confirmação;
* Token de redefinição;
* Data de criação.

O banco possui restrições para evitar a duplicidade de **nome de usuário** e **e-mail**.

### Reservas

Na versão atual do MVP, parte das informações relacionadas às reservas permanece sendo controlada pelo estado da sessão da aplicação.

Uma evolução futura será realizar a persistência completa das reservas diretamente no banco de dados.

---

## Autenticação e segurança

O sistema possui um mecanismo próprio de autenticação.

As senhas não são armazenadas diretamente no banco de dados.

É utilizado:

```text
PBKDF2-HMAC-SHA256
+ salt aleatório
+ comparação em tempo constante
```

Também são utilizados tokens para:

* Confirmação de e-mail;
* Recuperação e redefinição de senha.

As informações relacionadas ao servidor de e-mail podem ser configuradas por meio de variáveis de ambiente.

Quando um servidor SMTP não está configurado no ambiente de desenvolvimento, o projeto possui um mecanismo local para permitir os testes desses fluxos.

---

## Perfis de acesso

### Locatário

O Locatário possui acesso a:

* Dashboard;
* Busca de salas;
* Minhas Reservas;
* Favoritos;
* Perfil.

### Proprietário

O Proprietário possui acesso a:

* Dashboard;
* Cadastro de salas;
* Visualização das próprias salas;
* Reservas recebidas;
* Perfil.

### Administrador

O Administrador possui acesso ampliado e pode:

* Visualizar informações administrativas;
* Gerenciar contas;
* Alterar tipos de usuários;
* Confirmar contas;
* Bloquear usuários;
* Reativar usuários;
* Excluir contas;
* Acessar funcionalidades relacionadas ao gerenciamento do sistema.

---

## Design do sistema

O design foi desenvolvido buscando proporcionar uma experiência simples, organizada e intuitiva.

Foram considerados elementos como:

* Cores;
* Tipografia;
* Botões;
* Ícones;
* Cards;
* Menus;
* Formulários;
* Espaçamento;
* Organização das informações;
* Feedback visual após ações.

### Dashboard

O Dashboard apresenta informações resumidas em cards, permitindo rápida visualização dos principais dados.

Dependendo do perfil do usuário, podem ser apresentadas informações como:

* Reservas;
* Salas cadastradas;
* Próxima reserva;
* Reservas recebidas;
* Indicadores de utilização;
* Resumo de ocupação.

### Busca de salas

A busca permite informar:

* Data;
* Horário inicial;
* Horário final;
* Quantidade de pessoas.

Os resultados apresentam apenas as salas que atendem aos critérios utilizados na pesquisa.

---

## Responsividade

A interface foi planejada para proporcionar uma boa experiência em diferentes tamanhos de tela.

O sistema busca atender:

* Computadores;
* Notebooks;
* Tablets;
* Smartphones.

As funcionalidades essenciais devem permanecer acessíveis independentemente do dispositivo utilizado.

---

## Testes e validação

Durante o desenvolvimento, foram realizados testes e ajustes relacionados às principais funcionalidades.

Entre os itens analisados estão:

* Cadastro de usuário;
* Login com dados corretos;
* Login com dados incorretos;
* Confirmação de e-mail;
* Recuperação de senha;
* Acesso ao Dashboard;
* Busca de salas;
* Cadastro de salas;
* Navegação conforme o tipo de usuário;
* Gerenciamento de contas;
* Funcionamento do banco de dados;
* Integração entre Streamlit e as funcionalidades do projeto;
* Correções visuais e de ícones.

---

## Organização do projeto

A equipe utiliza uma divisão de responsabilidades para organizar o desenvolvimento.

As atividades envolvem:

```text
Planejamento
     ↓
Levantamento de requisitos
     ↓
Design
     ↓
Desenvolvimento
     ↓
Integração
     ↓
Testes
     ↓
Revisão
     ↓
Ajustes
```

O projeto utiliza **Git e GitHub** para manter o código compartilhado, registrar alterações e permitir a colaboração dos integrantes.

---

## Como executar o projeto

### Pré-requisitos

* Python instalado;
* Git instalado;
* Visual Studio Code ou outro editor de código.

### Clonar o repositório

```bash
git clone https://github.com/MarcosYnn/reserva_salas_asbranquelas.git
```

### Entrar na pasta

```bash
cd reserva_salas_asbranquelas
```

### Criar ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Executar o projeto

```bash
streamlit run app.py
```

---

## Links do projeto

### Aplicação

[ acessar Sistema de Reserva de Salas](https://reservasalasasbranquelas-znumjlvbtfpn9kejpwh5dl.streamlit.app/)

### Repositório

[Reserva de Salas — GitHub](https://github.com/MarcosYnn/reserva_salas_asbranquelas)

---

## Integrantes

* **Alexandre Amorim — Scrum Master:** responsável por auxiliar na organização e acompanhamento das atividades da equipe. Também participou do desenvolvimento da autenticação, revisão do código, ajustes no banco de dados e correções na interface de Login;

* **Arthur Coelho — Documentação:** responsável pela organização e atualização da documentação do projeto, registro das necessidades levantadas, requisitos, regras de negócio, critérios de aceitação e demais informações necessárias para manter o projeto documentado;

* **Emerson Castro — Back-end:** responsável pelo desenvolvimento das funcionalidades de Back-end. Participou da organização da estrutura MVC, desenvolvimento do Dashboard, autenticação, revisão do código, ajustes no banco de dados e correções técnicas;

* **Giullia Di Fátima — Front-end e Design:** responsável pelo desenvolvimento e organização visual da interface, atuando na criação do Design e no desenvolvimento do Front-end do sistema;

* **João Carlos Neres — Levantamento de Requisitos:** responsável pelo levantamento de requisitos com usuários, identificando necessidades e melhorias para o Sistema de Reserva de Salas;

* **Marcos Yan — Back-end:** responsável pelo desenvolvimento e integração das funcionalidades de Back-end, integração entre Streamlit e GitHub, testes de funcionalidade, organização da estrutura MVC, desenvolvimento do Dashboard e autenticação;

* **Paulo Nathan — Design:** responsável pelo desenvolvimento e apoio na criação visual do sistema, organização das telas e elementos da interface.

---

## Situação atual

O projeto já possui um MVP funcional e navegável desenvolvido utilizando Python e Streamlit.

Já estão implementados:

* Cadastro e autenticação de usuários;
* Confirmação de e-mail;
* Recuperação e redefinição de senha;
* Controle de acesso por perfil;
* Dashboard para Locatário;
* Busca de salas;
* Minhas Reservas;
* Favoritos;
* Perfil;
* Dashboard para Proprietário;
* Cadastro de salas;
* Visualização das próprias salas;
* Painel administrativo;
* Gerenciamento de usuários;
* SQLite para usuários e salas;
* Estrutura organizada em Controllers, Models, Views e Utils;
* Controle de versão utilizando Git e GitHub;
* Publicação da aplicação utilizando Streamlit.

É importante diferenciar as funcionalidades já implementadas das funcionalidades previstas no levantamento de requisitos.

Algumas áreas ainda estão em evolução, principalmente a persistência completa das reservas, manutenção de salas e aprimoramento dos filtros.

---

## Próximos passos

* Manter a documentação atualizada;
* Finalizar a persistência das reservas no banco de dados;
* Garantir que busca, reserva e cancelamento estejam integrados ao banco de ponta a ponta;
* Implementar controle completo de indisponibilidade;
* Implementar períodos de manutenção das salas;
* Melhorar os filtros por localização, capacidade e recursos;
* Ampliar as informações de acessibilidade;
* Melhorar a responsividade;
* Realizar testes de usabilidade;
* Realizar testes de integração;
* Criar testes para autenticação e regras de negócio;
* Revisar o código;
* Corrigir inconsistências visuais;
* Avaliar banco de dados remoto para utilização por múltiplos usuários;
* Preparar novas versões da aplicação;
* Manter GitHub e documentação sincronizados com a evolução do sistema.

---

## Conclusão

O desenvolvimento do **Sistema de Reserva de Salas** possibilita a aplicação prática dos conhecimentos adquiridos durante a disciplina de Programação Web, envolvendo planejamento, levantamento de requisitos, desenvolvimento de software, banco de dados, autenticação, segurança, interface e experiência do usuário.

A solução busca centralizar e simplificar o processo de utilização dos espaços disponíveis, permitindo localizar salas adequadas, consultar sua disponibilidade, organizar reservas e facilitar o gerenciamento dos ambientes.

A divisão das atividades entre os integrantes contribui para um desenvolvimento colaborativo, com responsabilidades relacionadas à documentação, levantamento de requisitos, Design, Front-end, Back-end, testes e organização da equipe.

O MVP atual já apresenta uma base funcional para evolução do projeto, com autenticação, diferentes perfis de acesso, gerenciamento de salas, busca, reservas e administração, permitindo que novas funcionalidades sejam incorporadas gradualmente.
