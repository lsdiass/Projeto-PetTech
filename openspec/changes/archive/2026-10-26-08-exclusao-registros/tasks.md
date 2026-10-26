# Tarefas: Exclusão Segura de Tutor, Pet e Serviço

## Backend (Xano)

- [x] **T-BK-01**: Impedir exclusão de Tutor inexistente ou com Pets vinculados e retornar confirmação explícita após exclusão válida.
- [x] **T-BK-02**: Impedir exclusão de Pet inexistente ou com Agendamentos vinculados e retornar confirmação explícita após exclusão válida.
- [x] **T-BK-03**: Impedir exclusão de Serviço inexistente ou com Agendamentos vinculados e retornar confirmação explícita após exclusão válida.
- [ ] **T-BK-04**: Validar diretamente no Xano exclusões válidas e rejeitadas para as três entidades, confirmando que relações e históricos são preservados.

## Frontend (Reflex)

- [x] **T-FT-01**: Oferecer ações de exclusão com confirmação e cancelamento nas listas de Tutor, Pet e Serviço.
- [x] **T-FT-02**: Integrar os três fluxos aos DELETEs, removendo itens somente após confirmação explícita ou GET individual retornando 404.
- [x] **T-FT-03**: Preservar itens e exibir mensagens de erro HTTP, status sem mensagem, falha de conexão e verificação inconclusiva.
- [x] **T-FT-04**: Validar a compilação Reflex e simular confirmação explícita, GET 404, cancelamento e rejeição do backend para os três fluxos.

## Documentação

- [x] **T-DOC-01**: Consolidar os requisitos de exclusão segura e integridade de Tutor–Pet e Pet/Serviço–Agendamento.
