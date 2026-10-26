# Design

## Contexto

As rotas `/pets` e `/servicos` possuem formulários de cadastro e listam os registros para edição por meio dos endpoints GET e PATCH do Xano. Registros antigos podem ter identificador válido, mas campos de domínio obrigatórios ausentes.

## Objetivos e não objetivos

**Objetivos:**

- Listar pets e serviços existentes nas telas correspondentes.
- Exibir e permitir corrigir registros legados identificáveis com dados obrigatórios ausentes.
- Abrir formulários de edição separados e pré-preenchidos.
- Validar os campos de domínio e relações no backend Xano.
- Manter os dados preenchidos em caso de falha ou resposta não confirmada.

**Fora do escopo:**

- Excluir pets, serviços ou agendamentos.
- Editar agendamentos, tutores ou outras entidades.
- Adicionar tabelas, entidades ou alterar regras de cadastro.

## Decisões

- Reutilizar `/pets`, `/servicos`, `GET /pet` e `GET /servico`, adicionando as listas abaixo dos formulários de cadastro.
- Manter formulários de edição separados dos formulários de cadastro para preservar rascunhos.
- Validar o identificador para montar cada item da lista, mas não descartar todos os registros quando um registro identificável tiver campos de domínio ausentes ou inválidos. Mostrar valores faltantes como vazios, sinalizar o item e permitir completá-lo na edição.
- Permitir editar todos os campos de negócio de Pet, incluindo Tutor. Raça e observações vazias serão enviadas como `null`.
- Permitir editar todos os campos de Serviço. Descrição vazia será enviada como `null`; nome deve ser não vazio, preço positivo e duração inteira positiva.
- Restringir os PATCH do Xano aos campos de negócio. Para Pet, verificar a existência do Pet e do Tutor informado antes da atualização.
- Confirmar respostas HTTP, identificador e todos os valores retornados antes de atualizar a lista. Em falha ou divergência, manter formulário e dados.
- Não oferecer exclusão nestas telas como parte desta change; os requisitos de exclusão são documentados separadamente em `exclusao-registros`.

## Riscos e trade-offs

- As listas dependem dos endpoints GET do Xano; falhas e respostas inválidas devem ser comunicadas.
- Registros sem identificador não podem ser selecionados para edição e são omitidos; registros com identificador permanecem acessíveis para correção.
- Os campos opcionais precisam aceitar `null` nos endpoints PATCH para permitir remoção de valores existentes.
