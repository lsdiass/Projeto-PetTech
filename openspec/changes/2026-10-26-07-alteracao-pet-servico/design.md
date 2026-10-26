# Design

## Contexto

As rotas `/pets` e `/servicos` exibem apenas formulários de cadastro. O Xano já possui endpoints GET para listar os registros e PATCH para atualizá-los, mas os PATCH atuais aceitam campos dinamicamente sem validação de domínio ou confirmação de existência.

## Objetivos e não objetivos

**Objetivos:**

- Listar pets e serviços existentes nas telas de cadastro correspondentes.
- Exibir e permitir corrigir registros legados com identificador válido e campos de domínio obrigatórios ausentes.
- Abrir formulários de edição separados e pré-preenchidos.
- Validar os campos de domínio e relações no backend Xano.
- Manter os valores no formulário em caso de falha ou resposta não confirmada.

**Fora do escopo:**

- Excluir pets ou serviços.
- Editar agendamentos, tutores ou outras entidades.
- Adicionar tabelas, entidades ou alterar regras de cadastro.

## Decisões

- Reutilizar `/pets`, `/servicos`, `GET /pet` e `GET /servico`, adicionando a listagem abaixo do cadastro.
- Manter as telas de edição separadas dos formulários de cadastro, para preservar rascunhos.
- Validar o identificador para montar cada item da lista, mas não descartar o conjunto inteiro quando um registro identificado tiver campos de domínio obrigatórios ausentes ou inválidos. Exibir os valores ausentes como vazios, sinalizar o item e permitir completá-lo na edição.
- Permitir editar todos os campos de negócio de Pet, incluindo tutor. Raça e observações vazias serão enviadas como `null` para permitir removê-las.
- Permitir editar todos os campos de Serviço. Descrição vazia será enviada como `null`; nome deve ser não vazio, preço numérico positivo e duração inteira positiva.
- Restringir os PATCH do Xano aos campos de negócio. Para Pet, verificar a existência do registro e do tutor informado antes de atualizar.
- Validar respostas HTTP, identificador e valores retornados antes de confirmar; atualizar a lista somente após confirmação.
- Não oferecer exclusão nas listas.

## Riscos e trade-offs

- As listas dependem da disponibilidade e do formato dos endpoints GET do Xano; erros e respostas inválidas serão apresentados sem mascarar dados como válidos.
- Registros sem identificador não podem ser selecionados para edição e são omitidos da lista; registros com identificador e dados incompletos permanecem acessíveis para correção.
- A atualização de campos opcionais exige que o PATCH aceite valores nulos explicitamente.
- Os dados exibidos dependem da resposta persistida pelo Xano; em caso de divergência, a edição permanece aberta para correção ou nova tentativa.
