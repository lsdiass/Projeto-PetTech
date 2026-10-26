# alteracao-pet-servico Specification

## Purpose

Definir a edição de pets e serviços existentes no Xano e nas respectivas telas, confirmando alterações somente quando o backend retornar os dados persistidos.

## Requirements

### Requirement: Editar pets existentes

O sistema MUST permitir alterar `tutor_id`, `nome`, `especie`, `raca`, `porte` e `observacoes_saude` de um pet existente por `PATCH /pet/{pet_id}`. O identificador deve ser positivo; o tutor deve existir; nome e espécie devem conter texto; e porte MUST ser `Pequeno`, `Médio` ou `Grande`. Raça e observações podem ser nulas. O backend MUST rejeitar dados inválidos ou pet/tutor inexistente sem atualizar registros.

#### Scenario: Alteração válida de pet

- **WHEN** o cliente envia os campos de Pet válidos e associa o registro a um tutor existente
- **THEN** o Xano atualiza somente os campos de negócio e retorna o pet atualizado com seu identificador

#### Scenario: Pet ou tutor inexistente e dados inválidos

- **WHEN** o identificador do pet ou tutor não existe, nome ou espécie está vazio, ou o porte não é permitido
- **THEN** o Xano rejeita a solicitação e não altera nenhum registro

### Requirement: Listar e selecionar pets para edição

A tela `/pets` MUST carregar pets por `GET /pet`, exibir uma ação **Editar** por registro com identificador válido e pré-preencher um formulário separado. Registros legados que tenham identificador válido, mas estejam sem campos obrigatórios, MUST permanecer visíveis, ser sinalizados como incompletos e permitir que o usuário os corrija. Deve informar carregamento, lista vazia e falha de listagem. Cancelar MUST encerrar a edição sem enviar PATCH, e a interface não deve oferecer exclusão.

#### Scenario: Abrir e cancelar edição de pet

- **WHEN** o usuário seleciona **Editar** em um pet listado
- **THEN** o formulário exibe os dados daquele pet; se cancelar, encerra a edição sem alterar o registro

#### Scenario: Falha ou resposta inválida na listagem de pets

- **WHEN** `GET /pet` falha ou retorna dados inválidos
- **THEN** a tela informa o problema e não apresenta a resposta como válida

#### Scenario: Pet legado com dados obrigatórios incompletos

- **WHEN** `GET /pet` retorna um pet com identificador válido, mas sem tutor, nome, espécie ou porte válido
- **THEN** a tela mantém esse pet na lista, indica que os dados estão incompletos e permite abrir a edição para preenchê-los

### Requirement: Editar serviços existentes

O sistema MUST permitir alterar `nome`, `descricao`, `preco` e `duracao_minutos` de um serviço existente por `PATCH /servico/{servico_id}`. O identificador deve ser positivo; nome não vazio; preço numérico maior que zero; duração inteira maior que zero. Descrição pode ser nula. O backend MUST rejeitar dados inválidos ou serviço inexistente sem atualizar o registro.

#### Scenario: Alteração válida de serviço

- **WHEN** o cliente envia nome não vazio, preço positivo, duração inteira positiva e descrição válida ou nula
- **THEN** o Xano atualiza somente os campos de negócio e retorna o serviço atualizado com seu identificador

#### Scenario: Serviço inexistente ou dados inválidos

- **WHEN** o identificador não existe, o nome está vazio, o preço não é positivo ou a duração é fracionária ou não positiva
- **THEN** o Xano rejeita a solicitação e não altera nenhum registro

### Requirement: Listar e selecionar serviços para edição

A tela `/servicos` MUST carregar serviços por `GET /servico`, exibir uma ação **Editar** por registro com identificador válido e pré-preencher um formulário separado. Registros legados que tenham identificador válido, mas estejam sem campos obrigatórios, MUST permanecer visíveis, ser sinalizados como incompletos e permitir que o usuário os corrija. Deve informar carregamento, lista vazia e falha de listagem. Cancelar MUST encerrar a edição sem enviar PATCH, e a interface não deve oferecer exclusão.

#### Scenario: Abrir e cancelar edição de serviço

- **WHEN** o usuário seleciona **Editar** em um serviço listado
- **THEN** o formulário exibe os dados daquele serviço; se cancelar, encerra a edição sem alterar o registro

#### Scenario: Falha ou resposta inválida na listagem de serviços

- **WHEN** `GET /servico` falha ou retorna dados inválidos
- **THEN** a tela informa o problema e não apresenta a resposta como válida

#### Scenario: Serviço legado com dados obrigatórios incompletos

- **WHEN** `GET /servico` retorna um serviço com identificador válido, mas sem nome, preço positivo ou duração inteira positiva
- **THEN** a tela mantém esse serviço na lista, indica que os dados estão incompletos e permite abrir a edição para preenchê-los

### Requirement: Confirmar somente alterações persistidas

As telas MUST confirmar sucesso e atualizar a lista somente se a resposta do PATCH contiver o identificador solicitado e todos os campos enviados correspondentes, incluindo valores nulos para campos opcionais limpos. Falhas HTTP, de conexão, respostas inválidas ou divergentes MUST ser informadas, mantendo o formulário e seus dados.

#### Scenario: Alteração confirmada

- **WHEN** o PATCH retorna o mesmo identificador e os campos correspondentes aos valores enviados
- **THEN** a interface confirma a alteração e atualiza somente o registro correspondente na lista

#### Scenario: Falha de confirmação

- **WHEN** o PATCH falha ou a resposta não confirma o identificador e os dados enviados
- **THEN** a interface informa a falha e mantém o formulário de edição preenchido
