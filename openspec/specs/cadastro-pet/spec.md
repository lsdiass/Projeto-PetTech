# cadastro-pet Specification

## Purpose

Definir o cadastro de pets no Xano e no frontend Petech, garantindo que cada pet seja associado a um tutor existente e que o sucesso exibido corresponda a um registro persistido.

## Requirements

### Requirement: Registrar pets vinculados a tutores existentes

O sistema MUST persistir cada pet na tabela `pet` com `tutor_id`, `nome`, `especie`, `raca`, `porte` e `observacoes_saude`, além dos campos técnicos padrão. `tutor_id`, `nome`, `especie` e `porte` são obrigatórios. `raca` e `observacoes_saude` são opcionais. O porte MUST ser um dos valores `Pequeno`, `Médio` ou `Grande`. O backend MUST rejeitar o cadastro se o tutor não existir ou se algum dado obrigatório for inválido, sem criar o registro.

#### Scenario: Cadastro válido

- **WHEN** o cliente envia `POST /pet` no grupo `Event Logs` com tutor existente, nome, espécie e porte válidos, e os campos opcionais preenchidos ou omitidos
- **THEN** o Xano grava o pet vinculado ao tutor e retorna o registro persistido com seu identificador

#### Scenario: Tutor inexistente

- **WHEN** o cliente envia `POST /pet` com um `tutor_id` que não corresponde a um tutor cadastrado
- **THEN** o Xano rejeita a entrada e não cria um registro

#### Scenario: Campo obrigatório ausente ou porte inválido

- **WHEN** o cliente envia `POST /pet` sem `tutor_id`, `nome`, `especie` ou `porte`, ou envia porte diferente de `Pequeno`, `Médio` ou `Grande`
- **THEN** o Xano rejeita a entrada e não cria um registro

### Requirement: Selecionar tutor cadastrado no formulário de Pet

O formulário de Pet MUST carregar as opções de tutor pelo endpoint `GET /tutor` do grupo `Event Logs` e MUST exigir a seleção de um tutor antes do envio. Se não houver tutores cadastrados ou se ocorrer falha ao carregar a lista, o formulário MUST informar a situação e não permitir cadastrar um pet sem tutor válido.

#### Scenario: Lista de tutores carregada

- **WHEN** o endpoint `GET /tutor` retorna tutores cadastrados
- **THEN** o formulário disponibiliza esses tutores para seleção e envia o identificador do tutor escolhido no cadastro

#### Scenario: Nenhum tutor disponível ou falha ao carregar

- **WHEN** não há tutores cadastrados ou `GET /tutor` retorna erro ou falha de conexão
- **THEN** o formulário informa que não é possível selecionar um tutor e não envia o cadastro como se tivesse sucesso

### Requirement: Confirmar apenas pets persistidos

O formulário MUST enviar os dados ao endpoint `POST /pet` do grupo `Event Logs`. MUST exibir sucesso e limpar os campos somente depois de receber um pet persistido com identificador e com os campos enviados `tutor_id`, `nome`, `especie` e `porte` correspondentes aos valores submetidos. Campos opcionais enviados também devem corresponder na resposta. Respostas HTTP de erro, falhas de conexão, respostas sem identificador ou respostas com campos ausentes ou divergentes não podem ser apresentadas como sucesso.

#### Scenario: Persistência confirmada

- **WHEN** o endpoint responde com sucesso e um pet contendo `id`
- **THEN** o formulário exibe confirmação do cadastro e limpa os campos

#### Scenario: Resposta sem identificador ou com dados ausentes

- **WHEN** o endpoint responde sem erro HTTP, mas não retorna um pet com `id` ou não retorna todos os dados obrigatórios enviados
- **THEN** o formulário informa que a gravação não foi confirmada e mantém os campos preenchidos

#### Scenario: Resposta com dados divergentes

- **WHEN** o endpoint retorna um pet com identificador, mas com tutor ou dados diferentes dos enviados
- **THEN** o formulário informa que os dados enviados não foram confirmados e mantém os campos preenchidos

#### Scenario: Falha de conexão ou HTTP

- **WHEN** o endpoint está indisponível ou retorna erro HTTP
- **THEN** o formulário exibe uma mensagem de erro e mantém os campos preenchidos
