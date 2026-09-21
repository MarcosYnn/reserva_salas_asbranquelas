# Sistema de Reserva de Salas

O **Sistema de Reserva de Salas** é um projeto acadêmico desenvolvido na disciplina de Programação Web.

A aplicação tem como objetivo facilitar o gerenciamento e a utilização dos espaços disponíveis em uma instituição, permitindo que usuários consultem salas, verifiquem horários disponíveis e realizem reservas de maneira simples, rápida e organizada.

O sistema busca reduzir processos manuais, evitar conflitos de horários e melhorar a visualização das informações relacionadas às salas e às reservas.

---

## Problema

Instituições que possuem diversas salas podem enfrentar dificuldades para organizar a utilização desses espaços.

Entre os principais problemas identificados estão:

- Dificuldade para consultar quais salas estão disponíveis;
- Falta de organização dos horários de utilização;
- Reservas duplicadas;
- Conflitos de horário;
- Dificuldade para localizar salas com determinadas características;
- Falta de informações sobre capacidade e recursos das salas;
- Falta de informações sobre salas temporariamente indisponíveis;
- Dependência de processos manuais para realizar reservas;
- Dificuldade para acompanhar reservas realizadas;
- Falta de uma área centralizada para gerenciamento dos espaços.

Essas dificuldades podem tornar o processo de reserva lento, confuso e sujeito a erros.

---

## Público-alvo

### Público principal

O sistema é destinado a usuários vinculados à instituição que necessitam utilizar salas para atividades acadêmicas, administrativas ou profissionais.

Entre os possíveis usuários estão:

- Alunos;
- Professores;
- Funcionários;
- Coordenadores;
- Colaboradores da instituição.

### Público administrativo

O sistema também poderá atender usuários responsáveis pelo gerenciamento das salas.

Esses usuários poderão:

- Cadastrar salas;
- Atualizar informações;
- Alterar a disponibilidade;
- Informar períodos de manutenção;
- Consultar reservas;
- Acompanhar a utilização dos espaços;
- Gerenciar informações relacionadas às salas.

---

## Proposta de solução

Desenvolver uma aplicação web que permita ao usuário:

- Realizar login no sistema;
- Consultar as salas disponíveis;
- Pesquisar salas por características;
- Utilizar filtros de busca;
- Visualizar capacidade, localização e recursos disponíveis;
- Consultar a disponibilidade por data e horário;
- Realizar reservas;
- Acompanhar as reservas realizadas;
- Cancelar reservas quando permitido;
- Visualizar avisos sobre salas indisponíveis;
- Identificar salas em manutenção;
- Obter informações claras sobre cada espaço;
- Utilizar o sistema tanto em computadores quanto em dispositivos móveis.

O sistema também deverá possuir uma área administrativa para gerenciamento das salas e acompanhamento das reservas.

---

## Objetivo do MVP

O MVP tem como objetivo entregar uma aplicação visual, navegável e funcional que demonstre o fluxo principal do Sistema de Reserva de Salas.

O fluxo principal deverá permitir que o usuário:

1. Acesse o sistema;
2. Visualize o Dashboard;
3. Consulte as salas cadastradas;
4. Pesquise ou filtre uma sala;
5. Consulte suas características;
6. Verifique a disponibilidade;
7. Selecione data e horário;
8. Confirme a reserva;
9. Consulte posteriormente suas reservas;
10. Cancele uma reserva quando permitido.

---

## Funcionalidades previstas

- Login de usuários;
- Dashboard principal;
- Consulta de salas;
- Busca de salas;
- Filtros por características;
- Visualização da capacidade das salas;
- Visualização dos recursos disponíveis;
- Visualização da localização;
- Identificação de recursos de acessibilidade;
- Consulta de disponibilidade;
- Seleção de data;
- Seleção de horário inicial e final;
- Realização de reservas;
- Confirmação de reservas;
- Visualização das reservas realizadas;
- Cancelamento de reservas;
- Identificação de salas indisponíveis;
- Avisos relacionados à manutenção;
- Área administrativa;
- Cadastro e atualização de salas;
- Gerenciamento da disponibilidade;
- Interface responsiva para computadores e celulares.

---

# Levantamento de Requisitos

## Requisitos funcionais

| Código | Requisito |
|---|---|
| RF01 | O sistema deve permitir o cadastro de usuários. |
| RF02 | O sistema deve permitir que o usuário realize login utilizando suas credenciais. |
| RF03 | O sistema deve apresentar um Dashboard após o acesso do usuário. |
| RF04 | O sistema deve permitir consultar as salas cadastradas. |
| RF05 | O sistema deve apresentar informações sobre cada sala, como nome ou número, capacidade, localização e recursos disponíveis. |
| RF06 | O sistema deve informar a situação atual de cada sala. |
| RF07 | O sistema deve permitir consultar a disponibilidade de uma sala. |
| RF08 | O sistema deve permitir selecionar uma sala para reserva. |
| RF09 | O sistema deve permitir selecionar a data da reserva. |
| RF10 | O sistema deve permitir selecionar o horário inicial e final da reserva. |
| RF11 | O sistema deve permitir informar a finalidade da reserva quando necessário. |
| RF12 | O sistema deve permitir confirmar uma reserva. |
| RF13 | O sistema deve registrar as reservas realizadas. |
| RF14 | O sistema deve permitir que o usuário consulte suas reservas. |
| RF15 | O sistema deve apresentar sala, data, horário e status das reservas realizadas. |
| RF16 | O sistema deve permitir cancelar uma reserva quando permitido. |
| RF17 | O sistema deve liberar novamente o horário depois do cancelamento de uma reserva. |
| RF18 | O sistema deve impedir reservas conflitantes para uma mesma sala e período. |
| RF19 | O sistema deve permitir buscar salas por características, como capacidade, localização e recursos disponíveis. |
| RF20 | O sistema deve permitir utilizar filtros para facilitar a localização de salas. |
| RF21 | O sistema deve permitir filtrar salas de acordo com a quantidade de pessoas. |
| RF22 | O sistema deve permitir identificar equipamentos e recursos existentes em cada sala. |
| RF23 | O sistema deve apresentar avisos sobre salas temporariamente indisponíveis. |
| RF24 | O sistema deve apresentar avisos sobre salas que estejam em manutenção. |
| RF25 | O sistema deve possuir uma área administrativa destinada a usuários autorizados. |
| RF26 | O administrador deve poder cadastrar salas. |
| RF27 | O administrador deve poder alterar informações das salas. |
| RF28 | O administrador deve poder alterar a disponibilidade das salas. |
| RF29 | O administrador deve poder informar períodos de manutenção. |
| RF30 | O administrador deve poder consultar as reservas realizadas. |
| RF31 | O sistema deve apresentar informações claras sobre os recursos disponíveis em cada sala. |
| RF32 | O sistema deve utilizar indicadores visuais para representar características das salas. |
| RF33 | O sistema deve apresentar informações relacionadas aos recursos de acessibilidade disponíveis. |
| RF34 | O sistema deve disponibilizar informações de apoio para facilitar a utilização da plataforma. |

---

## Requisitos não funcionais

| Código | Requisito |
|---|---|
| RNF01 | A interface deve ser simples, clara e intuitiva. |
| RNF02 | A navegação deve manter uma identidade visual consistente. |
| RNF03 | A aplicação deve possuir interface responsiva. |
| RNF04 | O sistema deve funcionar adequadamente em computadores, notebooks, tablets e smartphones. |
| RNF05 | As principais funcionalidades devem continuar acessíveis em dispositivos móveis. |
| RNF06 | As informações devem estar organizadas de forma que o usuário consiga localizar rapidamente as funcionalidades necessárias. |
| RNF07 | O sistema deve apresentar mensagens claras durante as operações realizadas pelo usuário. |
| RNF08 | Os botões e elementos interativos devem apresentar respostas visuais após as ações do usuário. |
| RNF09 | A interface deve apresentar de forma clara quando uma operação for concluída ou apresentar algum erro. |
| RNF10 | O acesso às funcionalidades administrativas deve ser restrito a usuários autorizados. |
| RNF11 | O sistema deve evitar conflitos e duplicidade de reservas. |
| RNF12 | A interface deve utilizar elementos visuais consistentes, como cores, ícones, botões, cards e formulários. |
| RNF13 | As informações sobre disponibilidade e indisponibilidade devem ser apresentadas de maneira clara e objetiva. |
| RNF14 | Os elementos da interface devem possuir tamanho, organização e espaçamento adequados para facilitar a interação. |
| RNF15 | O projeto deve utilizar Git e GitHub para controle de versão e colaboração da equipe. |
| RNF16 | As funcionalidades desenvolvidas devem seguir o protótipo aprovado pela equipe. |

---

## Regras de negócio

| Código | Regra |
|---|---|
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
| RN12 | Salas marcadas como indisponíveis não poderão receber novas reservas durante o período de indisponibilidade. |
| RN13 | Apenas usuários autorizados podem acessar a área administrativa. |
| RN14 | O administrador poderá cadastrar e atualizar informações relacionadas às salas. |
| RN15 | O sistema deve manter as informações de disponibilidade atualizadas após cada reserva ou cancelamento. |
| RN16 | O usuário deve visualizar as características da sala antes de concluir uma reserva. |

---

## Histórias de usuário

### HU01 — Login

Como usuário, quero acessar o sistema utilizando minhas credenciais para utilizar as funcionalidades da plataforma.

### HU02 — Consulta de salas

Como usuário, quero visualizar as salas cadastradas para escolher o espaço mais adequado para minha necessidade.

### HU03 — Busca por características

Como usuário, quero pesquisar salas por capacidade, localização e recursos disponíveis para encontrar rapidamente uma opção adequada.

### HU04 — Filtros de busca

Como usuário, quero utilizar filtros de busca para visualizar apenas as salas que atendem às minhas necessidades.

### HU05 — Recursos da sala

Como usuário, quero visualizar os recursos existentes em cada sala para saber se o espaço é adequado para a atividade que pretendo realizar.

### HU06 — Consulta de disponibilidade

Como usuário, quero consultar os horários disponíveis de uma sala para saber quando ela poderá ser utilizada.

### HU07 — Reserva de sala

Como usuário, quero selecionar uma sala, uma data e um horário para realizar uma reserva.

### HU08 — Acompanhamento

Como usuário, quero visualizar minhas reservas para acompanhar os espaços e horários reservados.

### HU09 — Cancelamento

Como usuário, quero cancelar uma reserva quando não precisar mais utilizar a sala.

### HU10 — Avisos

Como usuário, quero visualizar avisos sobre salas indisponíveis ou em manutenção para evitar selecionar um espaço que não possa ser utilizado.

### HU11 — Acessibilidade

Como usuário, quero visualizar informações sobre recursos de acessibilidade para saber se o espaço atende às minhas necessidades.

### HU12 — Gerenciamento de salas

Como administrador, quero cadastrar e atualizar as informações das salas para manter os dados do sistema atualizados.

### HU13 — Manutenção

Como administrador, quero informar quando uma sala estiver em manutenção para impedir reservas durante esse período.

### HU14 — Gerenciamento das reservas

Como administrador, quero consultar as reservas realizadas para acompanhar a utilização dos espaços disponíveis.

---

## Critérios gerais de aceitação

- Os campos obrigatórios devem ser validados;
- Dados inválidos devem apresentar mensagens claras;
- Usuários não autenticados não devem acessar áreas internas protegidas;
- O usuário deve conseguir visualizar as salas cadastradas;
- Cada sala deve apresentar suas principais características;
- O sistema deve permitir pesquisar salas;
- Os filtros devem alterar os resultados de acordo com os critérios selecionados;
- O sistema deve informar quando uma sala estiver disponível;
- O sistema deve informar quando uma sala estiver indisponível;
- O sistema deve informar quando uma sala estiver em manutenção;
- O usuário deve conseguir consultar a disponibilidade antes de reservar;
- O sistema não deve permitir duas reservas conflitantes para a mesma sala;
- Uma reserva confirmada deve aparecer na área de reservas do usuário;
- O cancelamento deve atualizar a situação da reserva;
- Após o cancelamento, o horário deve voltar a ficar disponível;
- Salas em manutenção não devem aceitar novas reservas no período informado;
- A área administrativa deve ser acessível somente por usuários autorizados;
- Os botões devem apresentar uma resposta perceptível após a interação;
- Mensagens de erro e sucesso devem ser apresentadas de forma clara;
- A interface deve se adaptar a diferentes tamanhos de tela;
- As funcionalidades essenciais devem funcionar tanto em computadores quanto em dispositivos móveis.

---

## Fluxo principal do usuário

O fluxo principal de utilização do sistema será:

```text
Login
  ↓
Dashboard
  ↓
Consultar Salas
  ↓
Pesquisar / Filtrar
  ↓
Selecionar Sala
  ↓
Visualizar Características
  ↓
Consultar Disponibilidade
  ↓
Selecionar Data e Horário
  ↓
Confirmar Reserva
  ↓
Minhas Reservas
