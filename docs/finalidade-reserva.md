# Finalidade da reserva

Card PraxiLab: [Adicionar finalidade da reserva](https://praxilab.io/ui/kanban/f586ceed-a963-4b0e-b219-aec5ed784726?s=board_saved#card-1844e81e-de39-4390-b2ec-d2b88f897013).

Base: main `c6bd29b`, com o PR #15 já integrado. Branch: `feature/arthur-finalidade-reserva`.

## Comportamento

O locatário pode preencher “Finalidade da reserva (opcional)” na busca ou no formulário de uma sala favorita. Exemplos: aula, reunião ou apresentação.

O campo aceita texto com até 500 caracteres após remoção de espaços nas extremidades. Texto vazio, apenas espaços ou ausência do parâmetro não impedem uma reserva. Tipos diferentes de texto são recusados pelo servidor; `None` é tratado como ausência do campo.

No Firestore, cada nova reserva recebe `finalidade` como string, inclusive vazia quando não informada. Reservas já existentes não precisam ser migradas. Nos detalhes de locatário, proprietário e administrador, a ausência de texto mostra “Não informada”.

O texto é apresentado com `st.text`, sem interpretar Markdown ou HTML. A finalidade acompanha a reserva quando seu status muda e não altera a detecção de conflitos, a regra de duplicação nem as permissões de consulta.

Editar a finalidade depois de uma busca envia o texto atual; isso não modifica o período escolhido. O formulário de Favoritos possui seu próprio campo e não reutiliza o texto da busca.

## Arquivos

| Arquivo | Alteração |
| --- | --- |
| models/reserva_firebase_model.py | Limite compartilhado, normalização, validação e persistência |
| controllers/reserva_controller.py | Validação antes da consulta e encaminhamento ao modelo |
| main.py | Campo opcional na busca e encaminhamento do texto atual |
| utils/componentes.py | Campo nos Favoritos e envio da finalidade nos dois fluxos |
| views/reserva_view.py | Exibição como texto simples e compatibilidade com registros antigos |
| tests/test_finalidade_reserva.py | Persistência, limites, tipos, legado e permissões reais dos filtros |
| tests/test_interface_finalidade.py | Busca, Favoritos, texto atualizado, três perfis e mensagens de erro |

## Validação automatizada

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Resultado local em 20/11/2026, Python 3.12: **87 testes aprovados e seis subtestes adicionais aprovados**. São 37 casos novos sobre a suíte de 50 testes da revisão final. Também foram verificadas a compilação Python e a integridade do diff.

| Grupo | Casos cobertos |
| --- | --- |
| Validação | Texto vazio, espaços, None, até 500 caracteres, 501 e tipos inválidos |
| Persistência | Criação e consulta, normalização e preservação após aprovação/cancelamento |
| Compatibilidade | Chamadas sem o novo parâmetro e registros existentes sem o campo |
| Autorização | Locatário consulta apenas seus pedidos; proprietário consulta suas salas; administrador consulta todos |
| Interface | Envio pela busca e Favoritos, alteração do texto após a busca, mensagens de erro e três perfis |
| Apresentação | Texto sem interpretação de Markdown/HTML e fallback “Não informada” |
| Regressão | Suíte anterior de datas, concorrência, sessões, favoritos e interface |

Os testes de dados utilizam armazenamento em memória com o decorator transacional real do SDK; AppTest testa a interface com serviços substituídos. Esses resultados não representam homologação no serviço Firebase publicado.

## Homologação após integração

Com contas e projeto Firebase de teste:

1. Buscar sala para período futuro, preencher finalidade, enviar e conferir o campo no documento persistido.
2. Repetir pelos Favoritos e confirmar que o formulário usa o texto e o período escolhidos nele.
3. Consultar o pedido como locatário, proprietário da sala e administrador.
4. Abrir uma reserva antiga sem `finalidade` e confirmar “Não informada”.
5. Confirmar que uma conta não visualiza reservas às quais não tem acesso.
6. Aprovar e cancelar o pedido; conferir preservação da finalidade e disponibilidade.
7. Validar campos, texto longo e navegação no celular.

O card deve permanecer em Revisão até a revisão do PR, integração e registro dos resultados de homologação exigidos pela equipe.
