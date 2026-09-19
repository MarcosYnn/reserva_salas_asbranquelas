# Sistema de Reserva de Salas

O **Sistema de Reserva de Salas** é um projeto acadêmico desenvolvido na disciplina de Programação Web.

A aplicação tem como objetivo facilitar o gerenciamento e a utilização das salas disponíveis em uma instituição, permitindo que os usuários consultem os espaços, verifiquem horários disponíveis e realizem reservas de maneira simples e organizada.

## Problema

Instituições que possuem diversas salas podem enfrentar dificuldades no controle e organização desses espaços.

Entre os principais problemas estão:

- Dificuldade para consultar quais salas estão disponíveis;
- Conflitos entre reservas realizadas no mesmo horário;
- Reservas duplicadas;
- Falta de organização dos horários de utilização;
- Dificuldade para localizar salas com determinadas características;
- Falta de informações sobre salas temporariamente indisponíveis;
- Dependência de processos manuais para realizar e controlar reservas.

Essas dificuldades podem tornar o processo de reserva lento, desorganizado e sujeito a erros.

## Público-alvo

### Público principal

Usuários vinculados à instituição que precisam consultar e reservar salas para utilização em determinados dias e horários.

Entre esses usuários podem estar:

- Alunos;
- Professores;
- Funcionários;
- Coordenadores;
- Colaboradores da instituição.

### Público administrativo

Usuários responsáveis pelo gerenciamento das salas e das reservas realizadas no sistema.

Esses usuários poderão:

- Cadastrar salas;
- Atualizar informações;
- Alterar a disponibilidade;
- Registrar períodos de manutenção;
- Consultar reservas;
- Gerenciar os espaços disponíveis.

## Proposta de solução

Desenvolver uma aplicação web que permita ao usuário:

- Realizar login no sistema;
- Consultar as salas disponíveis;
- Pesquisar salas de acordo com suas características;
- Visualizar capacidade e recursos disponíveis;
- Consultar a disponibilidade por data e horário;
- Realizar reservas;
- Acompanhar as reservas realizadas;
- Cancelar reservas quando permitido;
- Visualizar avisos sobre salas indisponíveis;
- Evitar conflitos de horários e reservas duplicadas.

O sistema também poderá disponibilizar uma área administrativa para o gerenciamento das salas e das reservas.

## Objetivo do MVP

O MVP tem como objetivo disponibilizar uma aplicação visual, navegável e funcional que demonstre o fluxo principal de reserva de salas.

O fluxo principal deverá permitir que o usuário:

1. Acesse o sistema;
2. Consulte as salas cadastradas;
3. Verifique a disponibilidade;
4. Escolha uma sala;
5. Informe data e horário;
6. Confirme a reserva;
7. Consulte suas reservas posteriormente.

## Funcionalidades do sistema

- Login de usuários;
- Dashboard principal;
- Consulta de salas;
- Visualização da capacidade das salas;
- Visualização dos recursos disponíveis;
- Consulta da localização da sala;
- Consulta de disponibilidade;
- Busca de salas por características;
- Seleção de data;
- Seleção de horário inicial e final;
- Realização de reservas;
- Confirmação de reservas;
- Visualização das reservas realizadas;
- Cancelamento de reservas;
- Identificação de salas indisponíveis;
- Avisos relacionados à manutenção;
- Área administrativa para gerenciamento das salas.

## Requisitos funcionais

| Código | Requisito |
|---|---|
| RF01 | O sistema deve permitir o cadastro de usuários. |
| RF02 | O sistema deve permitir que o usuário realize login utilizando suas credenciais. |
| RF03 | O sistema deve apresentar um Dashboard após o acesso do usuário. |
| RF04 | O sistema deve permitir consultar as salas cadastradas. |
| RF05 | O sistema deve apresentar informações sobre cada sala, como nome ou número, capacidade, localização e recursos disponíveis. |
| RF06 | O sistema deve informar a situação atual da sala. |
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
| RF17 | O sistema deve liberar novamente o horário após o cancelamento de uma reserva. |
| RF18 | O sistema deve impedir reservas conflitantes para uma mesma sala e horário. |
| RF19 | O sistema deve permitir buscar salas por características, como capacidade e recursos disponíveis. |
| RF20 | O sistema deve apresentar avisos sobre salas indisponíveis por manutenção. |
| RF21 | O sistema deve possuir uma área administrativa para usuários autorizados. |
| RF22 | O administrador deve poder cadastrar salas. |
| RF23 | O administrador deve poder alterar informações das salas. |
| RF24 | O administrador deve poder alterar a disponibilidade das salas. |
| RF25 | O administrador deve poder consultar as reservas realizadas. |

## Requisitos não funcionais

| Código | Requisito |
|---|---|
| RNF01 | A interface deve ser simples, clara e de fácil compreensão. |
| RNF02 | A navegação deve manter uma identidade visual consistente. |
| RNF03 | A aplicação deve possuir interface responsiva. |
| RNF04 | O sistema deve funcionar adequadamente em computadores, notebooks, tablets e smartphones. |
| RNF05 | As informações devem ser organizadas de forma que o usuário consiga encontrar rapidamente as funcionalidades necessárias. |
| RNF06 | O sistema deve apresentar mensagens claras durante as operações realizadas pelo usuário. |
| RNF07 | O acesso às funcionalidades administrativas deve ser restrito a usuários autorizados. |
| RNF08 | O sistema deve evitar conflitos e duplicidade de reservas. |
| RNF09 | A interface deve utilizar elementos visuais consistentes, como cores, botões, menus, cards e formulários. |
| RNF10 | O projeto deve utilizar Git e GitHub para controle de versão e colaboração da equipe. |

## Regras de negócio

| Código | Regra |
|---|---|
| RN01 | Somente usuários cadastrados devem realizar login no sistema. |
| RN02 | O usuário deve estar autenticado para utilizar as funcionalidades internas do sistema. |
| RN03 | Toda reserva deve estar associada a uma sala. |
| RN04 | Toda reserva deve possuir uma data definida. |
| RN05 | Toda reserva deve possuir horário inicial e horário final. |
| RN06 | Uma sala não pode possuir duas reservas para períodos conflitantes. |
| RN07 | Uma reserva somente pode ser confirmada quando a sala estiver disponível no período escolhido. |
| RN08 | Quando uma reserva for cancelada, o horário correspondente deve voltar a ficar disponível. |
| RN09 | Salas em manutenção devem ser apresentadas como indisponíveis para reserva. |
| RN10 | Apenas usuários autorizados podem acessar as funcionalidades administrativas. |
| RN11 | O administrador pode cadastrar, alterar e atualizar as informações das salas. |
| RN12 | O sistema deve apresentar ao usuário apenas horários disponíveis para reserva. |

## Histórias de usuário

### HU01 — Login

Como usuário, quero acessar o sistema utilizando minhas credenciais para utilizar as funcionalidades disponíveis.

### HU02 — Consulta de salas

Como usuário, quero visualizar as salas cadastradas para escolher o espaço mais adequado para minha necessidade.

### HU03 — Busca por características

Como usuário, quero pesquisar salas por capacidade e recursos disponíveis para encontrar uma sala adequada.

### HU04 — Consulta de disponibilidade

Como usuário, quero consultar os horários disponíveis de uma sala para saber quando posso utilizá-la.

### HU05 — Reserva de sala

Como usuário, quero selecionar sala, data e horário para realizar uma reserva.

### HU06 — Visualização das reservas

Como usuário, quero visualizar minhas reservas para acompanhar os espaços e horários que solicitei.

### HU07 — Cancelamento

Como usuário, quero cancelar uma reserva quando não precisar mais utilizar a sala.

### HU08 — Avisos

Como usuário, quero visualizar avisos sobre salas indisponíveis ou em manutenção para evitar tentar reservar um espaço que não pode ser utilizado.

### HU09 — Gerenciamento de salas

Como administrador, quero cadastrar e atualizar as informações das salas para manter os dados do sistema atualizados.

### HU10 — Gerenciamento das reservas

Como administrador, quero consultar as reservas realizadas para acompanhar a utilização dos espaços disponíveis.

## Critérios gerais de aceitação

- Os campos obrigatórios devem ser validados;
- Usuários sem autenticação não devem acessar áreas internas protegidas;
- O usuário deve conseguir visualizar as salas cadastradas;
- Cada sala deve apresentar suas principais informações;
- O sistema deve informar quando uma sala estiver indisponível;
- O usuário deve conseguir consultar a disponibilidade antes de reservar;
- O sistema não deve permitir duas reservas conflitantes para a mesma sala;
- Uma reserva confirmada deve aparecer na área de reservas do usuário;
- O cancelamento deve atualizar a situação da reserva;
- Após o cancelamento, o horário deve voltar a ficar disponível;
- Salas em manutenção devem aparecer como indisponíveis;
- A área administrativa deve ser acessível somente por usuários autorizados;
- A interface deve se adaptar a diferentes tamanhos de tela.

## Fluxo principal do usuário

O fluxo principal de utilização do sistema é:

```text
Login
  ↓
Dashboard
  ↓
Consultar Salas
  ↓
Selecionar Sala
  ↓
Consultar Disponibilidade
  ↓
Selecionar Data e Horário
  ↓
Confirmar Reserva
  ↓
Minhas Reservas
