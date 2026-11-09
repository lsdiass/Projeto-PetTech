## MODIFIED Requirements

### Requirement: Registrar tutores

O endpoint administrativo `POST /tutor` MUST continuar persistindo `nome`,
`email` e `telefone` na tabela `tutor`, com nome obrigatório e e-mail validado
quando informado. Os campos de conta `cpf` e `password` pertencem ao fluxo
separado de auto-cadastro de cliente; o endpoint administrativo não pode
retornar uma senha ou hash. A tabela permanece parte da entidade `Tutor`, sem
criar entidades adicionais.

#### Scenario: Cadastro administrativo preservado

- **WHEN** o cliente administrativo envia um tutor pela rota `POST /tutor`
- **THEN** o endpoint mantém a validação e a persistência existentes para nome,
  e-mail e telefone
- **AND** a resposta não contém senha nem hash

#### Scenario: Criar conta com credenciais

- **WHEN** um novo cliente envia CPF e senha pelo fluxo `/cliente/cadastro`
- **THEN** esses campos são persistidos somente pela operação de autenticação
  no Xano, sem alterar o contrato do endpoint administrativo `POST /tutor`
