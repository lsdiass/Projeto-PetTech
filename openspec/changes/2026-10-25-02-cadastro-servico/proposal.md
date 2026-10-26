# Cadastro de Serviços

## Por que

O domínio já prevê a entidade `Servico`, mas a tabela e o endpoint `POST /servico` ainda não persistem os dados comerciais. Sem o cadastro, o estabelecimento não consegue manter um catálogo utilizável nem informar preço e duração ao agendar atendimentos.

## O que muda

- Completa o schema da tabela `servico` com `nome`, `descricao`, `preco` e `duracao_minutos`.
- Implementa no endpoint `POST /servico` as validações no Xano para os dados obrigatórios e valores válidos.
- Adiciona no frontend Reflex uma tela de cadastro de serviços na rota `/servicos`.
- Adiciona navegação entre os cadastros existentes e o cadastro de serviços.
- Confirma o cadastro somente quando o Xano retornar o identificador e os dados do serviço persistido.
- Atualiza a documentação de domínio para registrar a descrição como atributo da entidade `Servico`.

## Capacidades

### Novas capacidades

- `cadastro-servico`: cadastro de serviços com preço e duração definidos.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: schema da tabela `servico` e endpoint `POST /servico` no grupo `Event Logs`.
- Frontend: `Petech/Petech.py`.
- Documentação: `docs/domain-model.md`.
- Não adiciona entidades ou tabelas e mantém o limite de quatro entidades (`Tutor`, `Pet`, `Servico` e `Agendamento`).
- Cadastro de profissionais não faz parte desta change.
