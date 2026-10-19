# Tarefas: Cadastro de Tutor

## Backend (Xano)
- [x] **T-BK-00**: Remover templates e endpoints antigos que referenciam tabelas fora do domínio.
- [x] **T-BK-01**: Atualizar schema da tabela `tutor` em `xano/table/tutor.xs` adicionando `nome`, `email` e `telefone`.
- [x] **T-BK-02**: Configurar validações de entrada no endpoint `POST /tutor` em `xano/api/event_logs/tutor_POST.xs`.
- [x] **T-BK-03**: Testar o endpoint `POST /tutor` via terminal; a requisição sem nome foi rejeitada com HTTP 400 e não criou registros.

## Frontend (Reflex)
- [x] **T-FT-01**: Criar o estado da página de cadastro (`TutorState`) para gerenciar inputs e status.
- [x] **T-FT-02**: Implementar o componente de formulário (inputs de Nome, E-mail, Telefone e botão de envio).
- [x] **T-FT-03**: Criar a função de integração `TutorState.signup_tutor` que faz a chamada `POST` para o Xano.
- [x] **T-FT-04**: Adicionar a página de cadastro à rota do app em `Petech/Petech.py`.
- [x] **T-FT-05**: Validar o preenchimento, envio e feedback com respostas simuladas de sucesso e de ausência de ID.
- [x] **T-FT-06**: Fixar a integração no `POST /tutor` do grupo `Event Logs` para impedir redirecionamento por configuração antiga e só confirmar sucesso quando a resposta incluir o ID persistido.
