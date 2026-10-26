# Exclusão Segura de Tutor, Pet e Serviço

## Por que

O sistema precisa permitir remover registros que não devem mais permanecer no cadastro sem deixar vínculos inválidos ou apagar o histórico de Agendamentos.

## O que muda

- Adiciona exclusão com confirmação explícita de Tutores, Pets e Serviços nas listas correspondentes.
- Impede no Xano excluir Tutor com Pet vinculado, ou Pet/Serviço com Agendamento vinculado.
- Não apaga dados relacionados em cascata.
- Confirma a exclusão por resposta explícita do Xano ou por consulta GET individual retornando 404 quando o DELETE não fornece confirmação reconhecível.
- Mantém o registro na lista e informa falhas quando a exclusão ou sua verificação não podem ser confirmadas.

## Capacidades

### Novas capacidades

- `exclusao-registros`: exclusão segura e confirmada de Tutores, Pets e Serviços.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: `DELETE /tutor/{tutor_id}`, `DELETE /pet/{pet_id}`, `DELETE /servico/{servico_id}` e GETs individuais do grupo `Event Logs`.
- Frontend: confirmação, estados e listas em `Petech/Petech.py`.
- OpenSpec: requisitos consolidados de exclusão segura das três entidades.
- Não adiciona entidades ou tabelas e não permite exclusão de Agendamentos.
