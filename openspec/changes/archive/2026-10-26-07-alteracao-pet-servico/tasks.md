# Tarefas: Alteração de Pet e Serviço

## Backend (Xano)

- [x] **T-BK-01**: Restringir `PATCH /pet/{pet_id}` aos campos de Pet e validar campos obrigatórios, porte permitido, registro existente e tutor existente.
- [x] **T-BK-02**: Restringir `PATCH /servico/{servico_id}` aos campos de Serviço e validar nome, preço positivo e duração inteira positiva.
- [ ] **T-BK-03**: Validar no Xano alterações válidas e rejeições de dados inválidos e identificadores inexistentes, sem atualização indevida.

## Frontend (Reflex)

- [x] **T-FT-01**: Listar pets e serviços identificáveis, informar estados de carregamento, lista vazia e falha, e sinalizar registros legados incompletos sem ocultá-los.
- [x] **T-FT-02**: Adicionar formulário pré-preenchido e ação de edição de Pet, preservando o cadastro existente e permitindo cancelar.
- [x] **T-FT-03**: Integrar Pet ao `PATCH /pet/{pet_id}`, confirmando ID e campos persistidos, inclusive nulos opcionais, e mantendo dados em caso de falha.
- [x] **T-FT-04**: Adicionar formulário pré-preenchido e ação de edição de Serviço, preservando o cadastro existente e permitindo cancelar.
- [x] **T-FT-05**: Integrar Serviço ao `PATCH /servico/{servico_id}`, confirmando ID e campos persistidos e mantendo dados em caso de falha.
- [x] **T-FT-06**: Validar compilação Reflex e fluxos de edição confirmada, resposta divergente, erro de carregamento e cancelamento.

## Documentação

- [x] **T-DOC-01**: Especificar requisitos verificáveis para listagem, edição, confirmação e correção de registros legados incompletos.
