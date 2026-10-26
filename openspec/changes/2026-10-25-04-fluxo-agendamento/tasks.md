# Tarefas: Fluxo de Agendamento

## Backend (Xano)

- [x] **T-BK-01**: Atualizar `xano/table/agendamento.xs` com `pet_id`, `servico_id`, `data_hora`, `status` e `observacoes_atendimento`, mantendo os campos técnicos existentes.
- [x] **T-BK-02**: Implementar endpoint mensal de disponibilidade por Serviço, retornando os inícios alinhados a 30 minutos e o estado de cada dia/horário, calculados a partir do expediente, feriados nacionais, duração do Serviço e intervalos não cancelados.
- [x] **T-BK-03**: Ajustar `xano/api/event_logs/agendamento_POST.xs` para validar existência de Pet e Serviço, data/horário, expediente, feriado e sobreposição; obter a duração no backend e gravar o status inicial `Agendado`.
- [x] **T-BK-04**: Verificar e documentar que `db.transaction` garante atomicidade, mas a documentação consultada não promete isolamento serializável ou bloqueio da vaga; concorrência simultânea ainda é uma limitação.
- [ ] **T-BK-05**: Após publicar os scripts aprovados no Xano, testar persistência válida, rejeição de referências inválidas, domingo/feriado, horário passado, fora do expediente, serviço que ultrapassa 18:00 e conflito por duração; confirmar que Cancelado libera o intervalo e que nenhum teste deixa registros residuais.
- [x] **T-BK-06**: Restringir o PATCH existente a status/observações para impedir alterações de Pet, Serviço ou horário que contornem a validação de agenda.
- [x] **T-BK-07**: Validar presença e tipo de `data_hora` e `duracao_minutos` antes de cálculos; receber `data_hora` como inteiro positivo em milissegundos e aplicar a mesma proteção às durações de Serviços já agendados na consulta e na criação.
- [x] **T-BK-08**: Delimitar com parênteses os resultados dos filtros XanoScript usados em comparações de alinhamento de minutos e dia da semana.

## Frontend (Reflex)

- [x] **T-FT-01**: Criar estado de agendamento para carregar Pets e Serviços e manter as seleções de Pet, Serviço, mês, dia e horário.
- [x] **T-FT-02**: Criar a rota `/agendamentos` com a sequência de seleção de Pet, Serviço e calendário mensal.
- [x] **T-FT-03**: Consultar a disponibilidade mensal no backend, desabilitando dias sem vagas e horários ocupados em cinza.
- [x] **T-FT-04**: Integrar a confirmação ao `POST /agendamento`, tratar conflito/falhas sem exibir sucesso, preservar as seleções e atualizar a consulta após uma falha.
- [x] **T-FT-05**: Exibir `Agendado com sucesso!` somente após confirmar o registro persistido e atualizar a disponibilidade.
- [x] **T-FT-06**: Adicionar navegação para o fluxo e validar a compilação Reflex.
- [x] **T-FT-08**: Evitar submissões repetidas e chamadas de disponibilidade automáticas após HTTP 429, erros 5xx, falhas de conexão ou respostas inválidas; orientar espera com `Retry-After` quando fornecido pelo Xano.
- [ ] **T-FT-07**: Validar interações reais com os endpoints Xano depois que os scripts locais forem publicados, incluindo conflito e confirmação.
