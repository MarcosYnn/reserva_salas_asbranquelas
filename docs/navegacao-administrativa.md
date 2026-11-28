# Cadastro e consulta de usuários no painel administrativo

## Correção de 28/11/2026

A opção Administração apresentava duas telas conforme o caminho utilizado. O atalho Cadastrar usuário abria o formulário completo; Consultar usuários guardava uma seção na sessão e abria uma lista com outro cadastro simplificado. Esse segundo formulário foi removido.

| Entrada | Destino |
| --- | --- |
| Administração, no menu | Formulário completo de cadastro |
| Cadastrar usuário, no Início | Mesmo formulário completo |
| Vamos começar, no Início | Mesmo formulário completo |
| Usuários cadastrados, acima de Administração no menu | Lista de contas com edição e exclusão mediante confirmação |
| Consultar usuários, no Início | Mesma lista de contas |

Sessões antigas com a seção usuarios em Administração passam para Usuários cadastrados na próxima renderização. O estado antigo é descartado para que o próximo acesso a Administração abra o cadastro completo.

A alteração organiza a interface administrativa. Os controladores existentes continuam responsáveis por autorizar operações no Firebase. Não há exclusão ou migração de contas como parte desta correção.

## Validação

Nove testes de interface com Streamlit AppTest cobrem:

- Ordem de Usuários cadastrados acima de Administração no menu.
- Lista acessível pelo menu e pelo atalho sem o cadastro simplificado.
- Cadastro completo acessível por Administração, Cadastrar usuário e Vamos começar.
- Sessão antiga e alternância posterior entre consulta e cadastro.
- Lista vazia sem reaparecimento do formulário removido.
- Edição de conta e confirmação obrigatória antes de habilitar exclusão.

```bash
python -m pytest -q tests/test_navegacao_admin.py
python -m pytest -q
```

Resultado local: **96 testes e 6 subtestes aprovados**, incluindo os 9 casos novos. As operações de dados são substituídas nos testes da interface; nenhuma conta real é criada, editada ou excluída por essa execução. A conferência da aplicação publicada deve ser feita depois da integração do PR.

Rastreabilidade: [Testes integrados e validação da entrega final — card 8768ae34-7f8a-4bb2-96ab-93d151ac6f4f](https://praxilab.io/ui/kanban/f586ceed-a963-4b0e-b219-aec5ed784726?s=board_saved#card-8768ae34-7f8a-4bb2-96ab-93d151ac6f4f).
