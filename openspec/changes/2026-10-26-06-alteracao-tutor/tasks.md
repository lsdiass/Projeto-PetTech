# Tarefas: Alteração de Tutor

## Backend (Xano)

- [x] **T-BK-01**: Restringir `PATCH /tutor/{tutor_id}` aos campos `nome`, `email` e `telefone`, validando nome não vazio e e-mail quando informado.
- [x] **T-BK-02**: Verificar a existência do Tutor antes da atualização e retornar erro de não encontrado sem alterar dados quando o identificador não existir.
- [ ] **T-BK-03**: Validar no Xano PATCH válido, e-mail inválido, nome vazio e identificador inexistente, sem alteração em casos inválidos.

## Frontend (Reflex)

- [x] **T-FT-01**: Carregar e validar a lista de tutores usando `GET /tutor`, exibindo estados de carregamento, vazio e erro.
- [x] **T-FT-02**: Adicionar ação **Editar** por tutor e formulário separado pré-preenchido, com opção para cancelar sem afetar o cadastro.
- [x] **T-FT-03**: Integrar o formulário ao `PATCH /tutor/{tutor_id}`, incluindo `null` para e-mail ou telefone vazios e tratando falhas sem limpar os dados.
- [x] **T-FT-04**: Confirmar somente respostas com identificador e campos correspondentes ao envio e atualizar a lista após persistência confirmada.
- [ ] **T-FT-05**: Validar a compilação Reflex e os fluxos de atualização confirmada e falha de confirmação.

## Documentação

- [x] **T-DOC-01**: Especificar os requisitos verificáveis de listagem, edição, validação e confirmação no capability `alteracao-tutor`.
