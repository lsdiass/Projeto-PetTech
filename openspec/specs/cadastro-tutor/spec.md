# cadastro-tutor Specification

## Purpose
Definir o cadastro de tutores no Xano e o feedback do formulário Petech, garantindo que o sucesso exibido corresponda a um registro persistido.

## Requirements

### Requirement: Registrar tutores

O sistema MUST persistir os dados do tutor na tabela `tutor`, limitada aos campos `nome`, `email` e `telefone` além dos campos técnicos padrão. O nome é obrigatório; o e-mail, quando informado, deve ser válido; telefone é texto e ambos são opcionais.

#### Scenario: Cadastro válido
- **WHEN** o cliente envia nome válido e os campos opcionais preenchidos ou omitidos para `POST /tutor` no grupo `Event Logs`
- **THEN** o Xano grava os dados na tabela `tutor` e retorna o registro persistido com seu identificador

#### Scenario: Nome ausente
- **WHEN** o cliente envia `POST /tutor` sem nome
- **THEN** o Xano rejeita a entrada e não cria um registro

#### Scenario: E-mail inválido
- **WHEN** o cliente envia um valor que não é um endereço de e-mail válido
- **THEN** o Xano rejeita a entrada e não cria um registro

### Requirement: Confirmar apenas cadastros persistidos

O formulário MUST enviar o cadastro ao endpoint `POST /tutor` do grupo `Event Logs` no workspace Xano do Petech. MUST exibir sucesso e limpar os campos somente depois de receber um registro persistido com identificador; respostas HTTP de erro, falhas de conexão ou respostas sem identificador não podem ser apresentadas como sucesso.

#### Scenario: Persistência confirmada
- **WHEN** o endpoint responde com sucesso e um tutor contendo `id`
- **THEN** o formulário exibe confirmação com o identificador e limpa os campos

#### Scenario: Resposta sem identificador
- **WHEN** o endpoint responde sem erro HTTP mas não retorna um tutor com `id`
- **THEN** o formulário informa que a gravação não foi confirmada e mantém os campos preenchidos

#### Scenario: Falha de conexão ou HTTP
- **WHEN** o endpoint está indisponível ou retorna erro HTTP
- **THEN** o formulário exibe uma mensagem de erro e mantém os campos preenchidos
