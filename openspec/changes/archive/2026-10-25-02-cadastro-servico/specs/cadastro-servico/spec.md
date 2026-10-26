# cadastro-servico Specification

## Purpose

Definir o cadastro de serviços no Xano e no frontend Petech, garantindo persistência dos dados comerciais e confirmação somente após receber o registro salvo.

## Requirements

### Requirement: Registrar serviços

O sistema MUST persistir cada serviço na tabela `servico` com `nome`, `preco` e `duracao_minutos`, além dos campos técnicos padrão. `descricao` é opcional. O nome MUST conter pelo menos um caractere não branco; `preco` MUST ser um valor numérico maior que zero; `duracao_minutos` MUST ser um número inteiro maior que zero, sem truncar valores fracionários. O backend MUST rejeitar entradas inválidas sem criar registros.

#### Scenario: Cadastro válido com descrição

- **WHEN** o cliente envia `POST /servico` no grupo `Event Logs` com nome válido, descrição preenchida, preço maior que zero e duração inteira positiva
- **THEN** o Xano grava os dados do serviço e retorna o registro persistido com seu identificador

#### Scenario: Cadastro válido sem descrição

- **WHEN** o cliente envia `POST /servico` com nome válido, descrição omitida, preço maior que zero e duração inteira positiva
- **THEN** o Xano grava o serviço sem descrição e retorna o registro persistido com seu identificador

#### Scenario: Nome ausente ou vazio

- **WHEN** o cliente envia `POST /servico` sem nome ou somente com espaços em branco
- **THEN** o Xano rejeita a entrada e não cria um registro

#### Scenario: Preço inválido ou não positivo

- **WHEN** o cliente envia `POST /servico` sem preço, com valor não numérico, zero ou valor negativo
- **THEN** o Xano rejeita a entrada e não cria um registro

#### Scenario: Duração inválida, fracionária ou não positiva

- **WHEN** o cliente envia `POST /servico` sem duração, com valor não numérico, fracionário, zero ou negativo
- **THEN** o Xano rejeita a entrada e não cria um registro

### Requirement: Confirmar apenas serviços persistidos

O formulário MUST enviar os dados ao endpoint `POST /servico` do grupo `Event Logs`. MUST exibir sucesso e limpar os campos somente depois de receber um registro com `id` e com `nome`, `preco` e `duracao_minutos` correspondentes aos valores enviados. Se uma descrição for enviada, o valor retornado também MUST corresponder. Respostas HTTP de erro, falhas de conexão, respostas sem identificador ou com campos ausentes ou divergentes MUST ser informadas como falha e manter os dados preenchidos.

#### Scenario: Persistência confirmada

- **WHEN** o endpoint responde com sucesso e retorna o serviço persistido com identificador e dados correspondentes
- **THEN** o formulário exibe confirmação e limpa os campos

#### Scenario: Resposta sem identificador ou com dados ausentes

- **WHEN** o endpoint responde sem erro HTTP, mas não retorna o serviço com identificador ou com todos os campos obrigatórios
- **THEN** o formulário informa que o cadastro não foi confirmado e mantém os campos preenchidos

#### Scenario: Falha de conexão ou HTTP

- **WHEN** o endpoint está indisponível ou retorna erro HTTP
- **THEN** o formulário exibe uma mensagem de erro e mantém os campos preenchidos
