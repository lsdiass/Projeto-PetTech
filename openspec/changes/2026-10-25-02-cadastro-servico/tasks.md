# Tarefas: Cadastro de Serviços

## Backend (Xano)

- [x] **T-BK-01**: Atualizar `xano/table/servico.xs` com `nome`, `descricao`, `preco` e `duracao_minutos`, preservando os campos técnicos existentes.
- [x] **T-BK-02**: Ajustar `xano/api/event_logs/servico_POST.xs` para receber os campos do serviço, exigir nome não vazio, preço maior que zero e duração inteira positiva, e persistir o registro.
- [ ] **T-BK-03**: Validar o endpoint `POST /servico` para cadastro válido e rejeição de nome ausente, preço inválido ou não positivo e duração inválida, fracionária ou não positiva, sem criação de registros inválidos.

## Frontend (Reflex)

- [x] **T-FT-01**: Criar o estado do cadastro de Serviço para gerenciar nome, descrição, valor, duração, envio e mensagens.
- [x] **T-FT-02**: Criar formulário na rota `/servicos` com nome, descrição opcional, valor e duração em minutos.
- [x] **T-FT-03**: Integrar o formulário ao `POST /servico`, convertendo o valor monetário de forma correta e tratando falhas HTTP, de conexão, respostas inválidas, sem ID ou com dados divergentes sem limpar os campos.
- [x] **T-FT-04**: Adicionar navegação para o cadastro de serviços nas telas de tutor e pet, preservando as rotas existentes.
- [x] **T-FT-05**: Validar a compilação Reflex e os estados de sucesso confirmado e falha de confirmação do cadastro.

## Documentação

- [x] **T-DOC-01**: Atualizar `docs/domain-model.md` com o atributo `descricao` da entidade `Servico`, mantendo as quatro entidades do domínio.
