# alteracao-tutor Specification

## Purpose

Definir a edição de tutores existentes no Xano e na tela `/tutores`, confirmando alterações somente quando o backend retornar os dados persistidos.

## Requirements

### Requirement: Atualizar os dados de um tutor existente

O sistema MUST permitir alterar somente `nome`, `email` e `telefone` de um registro existente da tabela `tutor`, por meio do endpoint `PATCH /tutor/{tutor_id}` do grupo `Event Logs`. O identificador deve ser positivo e corresponder a um tutor existente. `nome` é obrigatório e MUST conter texto após a remoção de espaços. `email` e `telefone` podem ser nulos; quando informado, `email` MUST ser válido. O backend MUST rejeitar a solicitação inválida ou de tutor inexistente sem alterar o registro.

#### Scenario: Alteração válida

- **WHEN** o cliente envia o identificador de um tutor existente, nome não vazio e e-mail e telefone válidos ou nulos
- **THEN** o Xano atualiza somente os campos de negócio do tutor e retorna o registro atualizado com seu identificador

#### Scenario: Identificador inexistente

- **WHEN** o cliente envia PATCH para um identificador que não corresponde a um tutor cadastrado
- **THEN** o Xano retorna erro de não encontrado e não altera nenhum registro

#### Scenario: Nome vazio ou e-mail inválido

- **WHEN** o cliente envia nome ausente/vazio ou um e-mail não nulo que não seja válido
- **THEN** o Xano rejeita a solicitação e não altera o tutor

### Requirement: Selecionar tutor para edição

A tela `/tutores` MUST carregar os registros pelo endpoint `GET /tutor`, apresentar uma ação **Editar** para cada tutor válido e pré-preencher um formulário separado com nome, e-mail e telefone. A tela MUST informar os estados de carregamento, lista vazia e falha de carregamento. A edição MUST oferecer cancelamento sem enviar alterações e não deve oferecer exclusão.

#### Scenario: Lista de tutores carregada

- **WHEN** `GET /tutor` retorna tutores válidos
- **THEN** a tela apresenta seus dados e permite abrir a edição de um tutor específico

#### Scenario: Falha ou resposta inválida na listagem

- **WHEN** `GET /tutor` falha ou retorna uma lista ou registro inválido
- **THEN** a tela informa que não conseguiu carregar os tutores e não apresenta a resposta como válida

#### Scenario: Cancelar edição

- **WHEN** o usuário cancela a edição de um tutor
- **THEN** o sistema encerra o formulário de edição sem enviar PATCH nem alterar o registro

### Requirement: Confirmar somente alterações persistidas

O formulário MUST enviar os três campos editáveis ao endpoint `PATCH /tutor/{tutor_id}`. E-mail e telefone vazios devem ser enviados como nulos. A interface MUST exibir sucesso e atualizar a lista somente quando a resposta contiver o identificador solicitado e os valores correspondentes ao formulário. Em falhas HTTP, de conexão, resposta inválida, ausência de identificador ou dados divergentes, a interface MUST informar que a alteração não foi confirmada e preservar os dados preenchidos.

#### Scenario: Alteração confirmada

- **WHEN** o PATCH retorna o tutor com identificador e campos correspondentes ao envio
- **THEN** a interface confirma a alteração e atualiza os dados daquele tutor na lista

#### Scenario: Falha HTTP, de conexão ou confirmação

- **WHEN** o PATCH falha, retorna resposta inválida ou não confirma o identificador e os valores enviados
- **THEN** a interface informa a falha e mantém o formulário e seus dados para correção ou nova tentativa
