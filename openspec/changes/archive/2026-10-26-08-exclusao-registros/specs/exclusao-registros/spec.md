# exclusao-registros Specification

## Purpose

Definir a exclusão segura e confirmada de Tutores, Pets e Serviços, preservando Pets e Agendamentos vinculados.

## Requirements

### Requirement: Excluir somente Tutores sem Pets vinculados

O endpoint `DELETE /tutor/{tutor_id}` do grupo `Event Logs` MUST aceitar somente identificadores positivos de Tutores existentes. O backend MUST impedir a exclusão quando houver qualquer Pet com `tutor_id` correspondente. Uma exclusão rejeitada MUST preservar o Tutor e todos os Pets. A operação MUST excluir somente o Tutor e retornar `{id, deleted: true}`.

#### Scenario: Tutor sem Pets

- **WHEN** o cliente solicita excluir um Tutor existente que não possui Pets vinculados
- **THEN** o Xano exclui somente o Tutor e retorna seu identificador com `deleted: true`

#### Scenario: Tutor inexistente ou com Pets

- **WHEN** o Tutor não existe ou possui Pets vinculados
- **THEN** o Xano rejeita a exclusão e preserva o Tutor e os Pets relacionados

### Requirement: Excluir somente Pets sem Agendamentos

O endpoint `DELETE /pet/{pet_id}` do grupo `Event Logs` MUST aceitar somente identificadores positivos de Pets existentes. O backend MUST impedir a exclusão se existir qualquer Agendamento com `pet_id` correspondente. Uma exclusão rejeitada MUST preservar o Pet e os Agendamentos. A operação MUST excluir somente o Pet e retornar `{id, deleted: true}`.

#### Scenario: Pet sem Agendamentos

- **WHEN** o cliente solicita excluir um Pet existente que não possui Agendamentos
- **THEN** o Xano exclui somente o Pet e retorna seu identificador com `deleted: true`

#### Scenario: Pet inexistente ou com Agendamentos

- **WHEN** o Pet não existe ou possui Agendamentos, inclusive cancelados
- **THEN** o Xano rejeita a exclusão e preserva o Pet e todos os Agendamentos

### Requirement: Excluir somente Serviços sem Agendamentos

O endpoint `DELETE /servico/{servico_id}` do grupo `Event Logs` MUST aceitar somente identificadores positivos de Serviços existentes. O backend MUST impedir a exclusão se existir qualquer Agendamento com `servico_id` correspondente. Uma exclusão rejeitada MUST preservar o Serviço e os Agendamentos. A operação MUST excluir somente o Serviço e retornar `{id, deleted: true}`.

#### Scenario: Serviço sem Agendamentos

- **WHEN** o cliente solicita excluir um Serviço existente que não possui Agendamentos
- **THEN** o Xano exclui somente o Serviço e retorna seu identificador com `deleted: true`

#### Scenario: Serviço inexistente ou com Agendamentos

- **WHEN** o Serviço não existe ou possui Agendamentos, inclusive cancelados
- **THEN** o Xano rejeita a exclusão e preserva o Serviço e todos os Agendamentos

### Requirement: Confirmar exclusão na interface

As listas de `/tutores`, `/pets` e `/servicos` MUST oferecer a ação **Excluir** sem enviar DELETE imediatamente, exigir confirmação explícita e oferecer cancelamento. A interface MUST remover o item somente após resposta bem-sucedida contendo o mesmo identificador solicitado e `deleted: true`. Se o DELETE retornar sucesso sem corpo ou sem confirmação válida, a interface MUST consultar o GET individual e confirmar a remoção somente se o Xano responder 404. Em erro HTTP, falha de conexão, registro ainda existente ou falha da verificação, MUST manter o registro visível e informar a falha. Se o corpo de erro não contiver mensagem legível, MUST apresentar o código HTTP.

#### Scenario: Cancelar exclusão

- **WHEN** o usuário cancela a confirmação de exclusão de Tutor, Pet ou Serviço
- **THEN** nenhum DELETE é enviado e o registro permanece na lista

#### Scenario: Confirmação explícita

- **WHEN** o usuário confirma e o Xano retorna o identificador correspondente com `deleted: true`
- **THEN** a interface informa sucesso e remove somente esse registro da lista

#### Scenario: Resposta sem confirmação no corpo

- **WHEN** o DELETE retorna sucesso HTTP, mas não retorna `{id, deleted: true}`
- **THEN** a interface consulta o GET individual e remove o registro somente se o Xano responder 404

#### Scenario: Exclusão não confirmada ou rejeitada

- **WHEN** o Xano rejeita a exclusão, o registro continua existindo ou a interface não consegue verificar o resultado
- **THEN** a interface mantém o registro na lista e apresenta a mensagem do backend, status HTTP ou erro de verificação
