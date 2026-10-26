# Design

## Contexto

A tela `/tutores` oferece somente o cadastro de tutores. O Xano já possui `GET /tutor`, para listar os registros, e `PATCH /tutor/{tutor_id}`, mas o PATCH atual aceita campos sem validação específica e não confirma que o tutor existe antes da tentativa de atualização.

## Objetivos e não objetivos

**Objetivos:**

- Listar os tutores existentes na tela atual.
- Permitir selecionar um tutor, carregar seus dados em um formulário de edição e atualizar nome, e-mail e telefone.
- Validar os dados e a existência do registro no backend Xano.
- Manter os campos preenchidos quando a alteração não for confirmada.

**Fora do escopo:**

- Editar Pets, Serviços ou Agendamentos.
- Adicionar entidades, tabelas ou módulos ao domínio.
- Alterar as regras do cadastro de tutor.

## Decisões

- Reutilizar a rota `/tutores` e o endpoint existente `GET /tutor`; adicionar a lista abaixo do formulário de cadastro.
- Abrir um formulário de edição separado e pré-preenchido ao selecionar **Editar**, preservando qualquer rascunho do formulário de cadastro.
- Enviar ao `PATCH /tutor/{tutor_id}` os campos `nome`, `email` e `telefone`. Nome deve conter texto após remoção de espaços; e-mail e telefone podem ser nulos para indicar que não foram informados.
- Restringir a atualização no Xano aos campos de negócio do Tutor e rejeitar identificador inexistente, nome vazio ou e-mail inválido antes de alterar o registro.
- Confirmar sucesso somente se a resposta contiver o identificador solicitado e os três valores correspondentes ao formulário. Em falhas HTTP, de conexão ou confirmação, manter a edição e os dados preenchidos.
- Atualizar a lista em memória somente após confirmação de persistência; a ação de cancelar encerra a edição sem enviar alterações.
- O Xano permanece responsável pela validação e integridade; validações no frontend servem apenas para feedback imediato.

## Riscos e trade-offs

- A tela depende do formato e da disponibilidade do endpoint existente `GET /tutor`; respostas inválidas ou falhas devem ser informadas sem ocultar um sucesso de alteração.
- O PATCH representa o conjunto completo de campos editáveis para permitir limpar e-mail ou telefone enviando `null`; a interface sempre envia os três campos.
