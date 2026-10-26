# Tarefas: Cadastro de Pet

## Backend (Xano)

- [x] **T-BK-01**: Atualizar `xano/table/pet.xs` com `tutor_id`, `nome`, `especie`, `raca`, `porte` e `observacoes_saude`, mantendo os campos técnicos existentes.
- [x] **T-BK-02**: Ajustar `xano/api/event_logs/pet_POST.xs` para receber os campos do cadastro, validar obrigatoriedade e valores permitidos para `porte`, confirmar a existência do tutor e persistir o registro vinculado.
- [ ] **T-BK-03**: Validar o endpoint `POST /pet` para cadastro válido e rejeição de tutor inexistente, dados obrigatórios ausentes e porte inválido, sem criação de registros inválidos.

## Frontend (Reflex)

- [x] **T-FT-01**: Criar o estado do cadastro de Pet para carregar tutores, manter os campos do formulário e representar carregamento, envio e erros.
- [x] **T-FT-02**: Criar o formulário na rota `/pets` com seleção obrigatória de tutor, nome, espécie e porte, além de raça e observações opcionais.
- [x] **T-FT-03**: Integrar o formulário ao `GET /tutor` existente e ao `POST /pet`, tratando erros HTTP, de conexão, resposta inválida, sem identificador ou com dados ausentes/divergentes sem limpar os campos.
- [x] **T-FT-04**: Adicionar navegação entre o cadastro de tutores existente e a nova tela de cadastro de pets, preservando a rota principal.
- [x] **T-FT-05**: Validar os estados de carregamento sem tutores, falha ao carregar tutores, sucesso com ID persistido e falhas no envio.
