# Tarefas: Cadastro de Pet e Agendamento no Dashboard

## Backend (Xano)

- [x] **T-BK-01**: Criar endpoint autenticado para cadastrar Pet vinculando-o exclusivamente ao Tutor autenticado.
- [x] **T-BK-02**: Criar endpoint autenticado para Agendamento, validando propriedade do Pet e as regras existentes de disponibilidade e conflito.
- [x] **T-BK-03**: Validar os scripts, revisar o vínculo do Pet no Xano e confirmar que os endpoints rejeitam chamadas sem autenticação.
- [x] **T-BK-04**: Publicar somente os endpoints aprovados após revisar o preview do Xano.

## Frontend (Reflex)

- [x] **T-FT-01**: Incluir IDs dos Pets do Tutor no estado privado do dashboard para seleção segura de Agendamento.
- [x] **T-FT-02**: Implementar formulário inline para cadastrar primeiro Pet e Pets adicionais, com validação, erros e confirmação.
- [x] **T-FT-03**: Implementar agendamento no dashboard com seleção de Pet próprio, Serviço, calendário, horários e confirmação.
- [x] **T-FT-04**: Atualizar dashboard e disponibilidade após gravação confirmada e preservar seleções em falhas.
- [x] **T-FT-05**: Manter o histórico somente leitura e distinguir estado vazio de erro.
- [x] **T-FT-06**: Compilar e testar payloads válidos/inválidos, falhas de sessão, isolamento do Pet, disponibilidade, status e confirmação.
- [ ] **T-FT-07**: Validar criação persistida de Pet e Agendamento usando uma conta de teste autorizada, sem criar dados reais de cliente.
- [x] **T-FT-08**: Enviar o token da sessão como `Bearer` nas chamadas autenticadas de cadastro de Pet e Agendamento; validar compilação e formato dos cabeçalhos.

## Documentação

- [x] **T-DOC-01**: Registrar as ações autenticadas do Tutor na visão do projeto.
