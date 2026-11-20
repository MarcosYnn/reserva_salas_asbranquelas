# Implementação da revisão final

Alterações desenvolvidas a partir da main 919feca, incorporando a revisão documental enviada pela equipe. Este documento descreve a branch de implementação; a disponibilidade no ambiente publicado depende da integração e da homologação.

## Reservas e coordenação das transações

O documento `salas/{sala_id}` é o ponto compartilhado de coordenação. Toda criação ou alteração de status de reserva lê esse documento e atualiza `reservas_atualizadas_em` na mesma transação que grava o pedido. A exclusão de sala também consulta os pedidos ativos e remove esse mesmo documento dentro de uma transação.

Na aprovação, a transação lê o pedido, a sala e os pedidos da mesma sala/data. Somente reservas aprovadas impedem a aprovação; pedidos pendentes concorrentes são permitidos para análise administrativa. A condição de sobreposição é `inicio_a < fim_b and fim_a > inicio_b`, permitindo horários adjacentes.

Se duas transações leem a mesma versão da sala, somente uma confirma primeiro; a outra precisa repetir as leituras pelo mecanismo de retry do SDK. Essa coordenação cobre também:

- Duplo clique na criação: mesmo UID/sala/data/início/fim não produz dois pedidos ativos.
- Cancelamento e aprovação concorrentes: disponibilidade é recalculada após retry.
- Criação concorrente com exclusão da sala: o pedido não é confirmado para uma sala removida.
- Aprovação de pedido antigo: período e existência da sala são revalidados.

Todas as leituras precedem as escritas da transação. A implementação coordena toda a sala, inclusive datas diferentes; é uma escolha conservadora adequada ao volume esperado do projeto, com potencial de contenção em alta concorrência. O protocolo exige que os escritores de reservas usem o código atualizado. Alterações manuais no console e aplicações antigas que gravem diretamente não participam da coordenação.

Não há migração destrutiva de dados. Pedidos existentes usam a mesma coleção; a primeira alteração passa a atualizar o documento da sala. Registros aprovados com períodos inválidos impedem uma aprovação sobreposta de ser liberada silenciosamente e exigem revisão dos dados.

## Identidade e permissões

O login compara o UID do documento do perfil ao UID da conta autenticada e do token verificado. Antes de ações protegidas, o servidor consulta o perfil por UID e consulta a conta no Firebase Authentication. Conta inativa, removida, divergente ou com perfil inválido não mantém autorização.

Mudança de perfil ou login limpa navegação e dados associados à conta e atualiza o usuário em uso. Bloqueio ou falha de verificação impede a ação; não há autorização por cache após erro. A revalidação acontece na próxima interação, sem atualização remota automática de abas inativas.

O logout e um login bem-sucedido limpam filtros, resultados, favoritos em memória, páginas selecionadas, rotas e widgets da conta anterior. Somente a inicialização técnica e a lista de salas são preservadas.

## Favoritos, busca e interface

- Favoritos ficam em `usuarios/{uid}/favoritos/{sala_id}`, com cópia na sessão para renderização.
- Reservar pelos Favoritos abre formulário próprio com data, início e fim; não utiliza o último período da busca.
- Resultados e período da busca são invalidados quando qualquer filtro muda.
- Filtros de capacidade, localização e recursos são aplicados em conjunto.
- Sala, nome e proprietário são consultados novamente na transação de criação.
- Erro ao consultar disponibilidade não produz resultados apresentados como validados.
- Próxima reserva considera apenas aprovação com início futuro.
- Administrador edita e exclui salas de todos os proprietários; proprietários continuam limitados às suas.
- Mapa aparece nos três perfis e verifica acesso explicitamente.
- Agenda, Suporte e Notificações provisórios foram retirados do menu administrativo.

## Ambiente e execução

Python 3.12; dependências diretas fixadas em requirements.txt. O fuso padrão é `America/Porto_Velho`, configurável por `APP_TIMEZONE`. A dependência tzdata permite utilizar o mesmo identificador em ambientes sem banco de fusos do sistema, incluindo Windows.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Resultado local: **50 testes passaram, com seis subtestes adicionais aprovados**. Também foram conferidas a compilação Python e a ausência de erros de whitespace no diff. O workflow de CI está em `.github/workflows/tests.yml`; seu resultado remoto deve ser verificado no PR.

| Área | Validação executada |
| --- | --- |
| Datas | Passado, início já ocorrido, futuro, término inválido e formatos canônicos |
| Transações | Sobreposição, adjacência, datas/salas distintas, duplo clique, cancelamento, titularidade, sala removida e concorrência |
| Sessões | UID divergente, bloqueio, exclusão, rebaixamento, erro de consulta, logout e novo login |
| Favoritos | Persistência por UID, isolamento entre contas e sala removida |
| Interface | AppTest: alteração de filtros, recursos/localização, período próprio nos Favoritos e falha de consulta |

Os testes transacionais importam o SDK e utilizam o decorator transacional real sobre armazenamento MVCC em memória, incluindo conflito de versões, retries e rollback. Não acessam o serviço Firestore. Os testes de interface exercitam as páginas de busca e favoritos com serviços substituídos por mocks.

## Card de homologação

**Título:** Homologar correções da revisão final com Firebase

**Prioridade:** Alta

**Dependência:** integração da branch de implementação.

- [ ] Executar os roteiros T01–T18 com projeto e contas de teste.
- [ ] Aprovar dois pedidos sobrepostos em sessões independentes; no máximo um deve ser aprovado.
- [ ] Repetir envio do mesmo período e verificar existência de apenas um pedido ativo.
- [ ] Cancelar reserva e aprovar outra sobreposta.
- [ ] Bloquear, excluir ou alterar perfil de conta conectada; a próxima ação deve respeitar a alteração.
- [ ] Alternar duas contas no mesmo navegador e conferir isolamento dos favoritos e filtros.
- [ ] Abrir nova sessão da mesma conta e conferir favoritos persistidos.
- [ ] Validar mapa nos três perfis e calendário após aprovação/cancelamento.
- [ ] Conferir edição/exclusão de salas pelo administrador e restrição do proprietário.
- [ ] Testar computador/celular e registrar capturas, resultados e responsáveis.
- [ ] Vincular PR, commits e evidências aos IDs reais dos cards do PraxiLab.

Não marcar este card como concluído com base apenas nos testes locais.

## Pendências fora desta implementação

Manutenção/indisponibilidade, finalidade do pedido, informações de acessibilidade, edição do próprio perfil e recuperação de senha continuam dependentes de definição de escopo e desenvolvimento. O vínculo do proprietário da sala ainda utiliza login; uma migração para UID precisa considerar os dados existentes. A proteção do último administrador ativo ainda não é transacional.
