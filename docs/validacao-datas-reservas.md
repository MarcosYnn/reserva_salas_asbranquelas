# Validação de datas e horários de reservas

Card relacionado: **Revisão do código**, no Kanban do PraxiLab. O responsável deve anexar o identificador e o link real do card ao PR e registrar a entrega no quadro.

## Problema e comportamento esperado

O modelo validava o formato da data e a ordem dos horários, mas aceitava reservas para dias anteriores e horários que já começaram hoje.

A validação em `models/reserva_firebase_model.py` passa a rejeitar:

- Datas anteriores ao dia atual.
- Horários iniciais que já começaram, quando a reserva é para hoje.
- Horário final igual ou anterior ao inicial.
- Datas ou horários em formato inválido.

Reservas para hoje com início futuro e reservas para dias futuros continuam permitidas. A validação ocorre antes da gravação do pedido no Firestore, incluindo os pedidos feitos pelos Favoritos.

## Relógio utilizado

A regra usa `datetime.now()`, o relógio local do servidor, acompanhando a referência atual da aplicação (`date.today()` nas páginas). O início precisa ser posterior ao instante atual; um minuto que já começou é considerado passado.

O fuso do ambiente deve ser conferido antes da validação no site publicado. A adoção de um fuso institucional explícito e consistente em toda a aplicação é uma configuração a definir pela equipe.

## Testes de regressão

Instale as dependências do projeto e execute, na raiz:

~~~bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "test_validacao_datas_reservas.py" -v
~~~

Os testes usam relógio fixo em 10/05/2030 às 12:00:30 e não chamam operações do Firestore. As dependências Firebase/Streamlit são necessárias para importar o módulo.

| Cenário | Esperado |
| --- | --- |
| Dia anterior | Recusar |
| Hoje, início às 11h | Recusar |
| Hoje, início às 12h | Recusar: o minuto já começou |
| Hoje, início às 12h01 | Aceitar |
| Amanhã, das 8h às 9h | Aceitar |
| Término anterior ou igual ao início | Recusar |
| Data inválida ou ausente | Recusar com mensagem de formato |
| Horário inválido ou ausente | Recusar com mensagem de formato |

**Situação em 16/11/2026:** testes preparados, execução pendente porque o ambiente de execução da sessão está indisponível. Não registrar como aprovados até executá-los.

## Conferência manual

Em um projeto Firebase de teste, tentar reservar ontem e hoje em horário passado. Confirmar que a mensagem é apresentada e que nenhum documento é criado para a tentativa inválida. Depois solicitar um horário futuro e verificar que o pedido é gravado como Pendente. Registrar ambiente, fuso, data, responsável e resultado no card.

Esta alteração não modifica pedidos existentes, aprovação de conflitos, bloqueio de contas ou o layout da busca.
