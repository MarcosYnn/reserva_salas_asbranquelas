# Validação integrada — 20/11/2026

## Ambiente e alcance

- Aplicação: https://reservasalasasbranquelas-znumjlvbtfpn9kejpwh5dl.streamlit.app/
- Projeto Firebase conectado: `reservas-salas-asbranquelas`; banco Firestore `(default)`.
- Base de código consultada e usada na suíte local: main `4899dd98ac0721e7a4bd288515f36df711d692c2`, com PRs [#15](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/15) e [#16](https://github.com/MarcosYnn/reserva_salas_asbranquelas/pull/16) integrados.
- A aplicação publicada foi testada pelo navegador. Não foi obtida identificação independente do SHA do processo publicado; a base informada acima é a do repositório e da suíte.
- Execução conduzida por Arthur com apoio de automação, usando contas fornecidas pelo usuário. A segunda conta de teste, `locatario_arthur_2`, foi cadastrada pelo usuário no painel administrativo e teve o login confirmado.
- Foram usados o projeto existente da equipe e pedidos novos identificados como TESTE. Não houve ambiente Firebase isolado provisionado nesta execução.
- Suíte automatizada já executada nesta base: **87 testes e 6 subtestes aprovados**, Python 3.12, dependências de `requirements-dev.txt`. Firestore simulado e AppTest; não são 87 testes contra o serviço remoto.

## Rastreabilidade

| Card PraxiLab | Escopo |
| --- | --- |
| [Testes integrados e validação da entrega final](https://praxilab.io/ui/kanban/f586ceed-a963-4b0e-b219-aec5ed784726?s=board_saved#card-8768ae34-7f8a-4bb2-96ab-93d151ac6f4f) | Execução manual, resultados e limites |
| [Nova documentação](https://praxilab.io/ui/kanban/f586ceed-a963-4b0e-b219-aec5ed784726?s=board_saved#card-813c3f4d-7020-410a-8d5e-1892c6f265af) | Atualização do README e deste registro |
| [Adicionar finalidade da reserva](https://praxilab.io/ui/kanban/f586ceed-a963-4b0e-b219-aec5ed784726?s=board_saved#card-1844e81e-de39-4390-b2ec-d2b88f897013) | Campo opcional e compatibilidade com legado |

Os resultados também foram acrescentados ao card Revisão do código. Documentação e testes não comprovam, por si, o mínimo individual de commits exigido pelo professor.

## Resultados observados na aplicação real

| ID | Procedimento | Resultado observado |
| --- | --- | --- |
| V01 | Abrir a aplicação sem sessão e tentar credenciais incorretas | Tela de login sem menu interno; credenciais incorretas recusadas. Não equivale a auditoria de acesso direto a todas as rotas |
| V02 | Entrar como Administrador e como dois Locatários | Menus correspondentes aos perfis; Locatário sem opção Administração |
| V03 | Consultar salas, reservas e detalhes de registro antigo | Três salas e cinco reservas anteriores aos testes consultadas; reserva sem finalidade exibiu “Não informada” |
| V04 | Buscar ou solicitar pelos Favoritos usando hoje às 09:00, já passado no momento do teste | Operação bloqueada: “Para hoje, o horário inicial deve ser posterior ao horário atual.” |
| V05 | Criar pedido pela busca para 21/11, 09:00–10:00, com finalidade; repetir sala/período na mesma conta | Primeiro pedido persistido; repetição bloqueada: “Você já tem um pedido ativo para esta sala e período.” |
| V06 | Cancelar V05 e repetir pela busca com finalidade vazia | Novo pedido aceito, campo persistido como string vazia e detalhes com “Não informada”; segundo pedido também cancelado |
| V07 | Favoritar Sala de Treinamento, consultar lista e abrir Reservar | Uma sala na lista; formulário próprio iniciou em 20/11, sem reutilizar a data de 21/11 da busca anterior |
| V08 | Pelo favorito, escolher 22/11, 09:00–10:00, e finalidade própria | Pedido enviado e depois consultado pelo administrador; texto e período confirmados no Firestore |
| V09 | Entrar na conta nova enquanto a primeira tem favorito e pedidos | Conta nova começou sem reservas/favoritos da primeira; após seu pedido, cada conta continuou vendo somente suas reservas |
| V10 | Segunda conta pedir a mesma sala em 22/11, 09:30–10:30 | Busca sinalizou sobreposição e permitiu pedido Pendente para análise |
| V11 | Administrador aprovar 09:00–10:00 e tentar aprovar 09:30–10:30 | Segunda aprovação bloqueada: “Já existe uma reserva aprovada que ocupa este horário.” |
| V12 | Administrador cancelar 09:00–10:00 e aprovar 09:30–10:30 | Segunda aprovação aceita; finalidade preservada nos detalhes |
| V13 | Abrir calendário da segunda conta, cancelar sua reserva aprovada e reabrir calendário | Evento inicialmente exibido no dia 22; após cancelamento pelo titular, calendário sem reservas confirmadas |
| V14 | Consultar os dois documentos de 22/11 no console e remover o favorito criado | UIDs solicitantes distintos; finalidades corretas; ambos Cancelada. Lista de favoritos voltou a ficar vazia |

V09 verifica consultas expostas pela interface com contas de nomes distintos. Não comprova sozinho todos os controles de autorização nem o caso de nomes iguais. Não foram tentadas operações diretas sobre documentos alheios.

## Sequência do conflito

1. Primeira conta enviou o pedido A (22/11, 09:00–10:00) pelos Favoritos.
2. Segunda conta enviou o pedido B (22/11, 09:30–10:30) pela busca; ambos puderam ficar pendentes.
3. Administrador aprovou A.
4. Aprovação de B foi recusada e B permaneceu pendente.
5. Administrador cancelou A.
6. Administrador aprovou B; o calendário do titular passou a exibi-lo.
7. Titular cancelou B; o calendário deixou de exibi-lo.

**Este foi um teste sequencial.** Não houve aprovação simultânea por dois decisores nem medição de carga ou latência.

## Documentos para conferência

Coleção `reservas`, no projeto da equipe:

| Documento | Fluxo e período | Estado final conferido |
| --- | --- | --- |
| `npQufHYq078SE6X7GUTi` | Busca, finalidade preenchida; 21/11 09:00–10:00 | Cancelada |
| `Kf5Ex1Nk5qFS8PGmnKtE` | Busca, finalidade vazia; 21/11 09:00–10:00 | Cancelada |
| `1Pqk1SqxYQvCvDOM1oVy` | Pedido A pelos Favoritos; 22/11 09:00–10:00 | Cancelada |
| `YVCY8mmXcJc7lxdFxkXq` | Pedido B da segunda conta; 22/11 09:30–10:30 | Cancelada |

Os documentos comprovam os campos e estados finais; não mantêm um histórico completo de cada clique ou de todas as transições. A mensagem de bloqueio e as etapas intermediárias foram observadas na interface e registradas neste relato e no PraxiLab. Não foram anexadas capturas ou exportações nesta atualização.

Nenhum pedido criado nesta validação ficou ativo. Os registros cancelados foram preservados. O favorito de teste foi removido. A conta `locatario_arthur_2` permanece cadastrada para continuidade dos testes; suas credenciais e dados pessoais não fazem parte deste documento.

## Limitações e próximos cenários

- Perfil Proprietário: suas páginas, escopo de salas e permissões de decisão.
- Aprovações realmente simultâneas no serviço remoto; adjacência e demais combinações de períodos no ambiente publicado.
- Favoritos após nova autenticação da mesma conta e alternância de contas na mesma sessão do navegador.
- Contas com nomes iguais, bloqueio/rebaixamento em sessão ativa e falhas de consulta no serviço.
- Edição/exclusão de contas, proteção do último administrador e históricos de salas removidas.
- Texto longo nos formulários publicados, visualização da finalidade pelo Proprietário e limites do campo no celular.
- Responsividade, contraste, navegação móvel e percurso completo do mapa nos três perfis.

Os testes locais cobrem parte desses comportamentos com armazenamento simulado. Manter os casos manuais como pendentes até obter resultado real ou registrar decisão de escopo da equipe.

## Reprodução

Utilizar contas de teste autorizadas, uma sala existente e uma data futura. Se repetir depois de 22/11/2026, escolher outro dia futuro, identificar os pedidos como TESTE e usar os mesmos intervalos relativos. Confirmar o estado de cada pedido na aplicação e no Firestore; cancelar todos os pedidos de teste ao encerrar. Não registrar senhas, tokens, chaves ou informações pessoais em cards, commits ou capturas.
