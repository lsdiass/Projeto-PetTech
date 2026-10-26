# Design

## Contexto

A entidade `Servico` está definida no modelo de domínio com nome, preço e duração, mas a tabela `servico` contém somente os campos técnicos `id` e `created_at`. O endpoint `POST /servico` também não recebe nem grava dados comerciais. A aplicação Reflex apresenta atualmente telas de cadastro de tutores e pets.

## Objetivos e não objetivos

**Objetivos:**

- Persistir os dados do catálogo de serviços na entidade existente `Servico`.
- Validar no backend os dados recebidos antes de gravar.
- Disponibilizar um formulário Reflex acessível pela rota `/servicos`.
- Confirmar sucesso somente após a resposta do Xano comprovar os dados persistidos.

**Fora do escopo:**

- Criar a entidade `Profissional` ou qualquer quinta entidade.
- Cadastrar, editar ou associar funcionários aos serviços.
- Implementar edição, exclusão, listagem ou gerenciamento de disponibilidade dos serviços.
- Alterar endpoints de agendamento nesta change.

## Decisões

- Usar os campos `nome`, `descricao`, `preco` e `duracao_minutos`, mantendo os nomes do domínio e exibindo `preco` como valor monetário na interface.
- Tornar `nome`, `preco` e `duracao_minutos` obrigatórios; manter `descricao` opcional para serviços cujo nome já seja suficiente para identificá-los.
- Exigir nome não vazio, preço numérico maior que zero e duração inteira maior que zero.
- Implementar as validações exclusivamente no backend Xano; a interface pode antecipar feedback, mas não substitui a validação do endpoint.
- Manter o preço como valor decimal no backend e na submissão; formatar a entrada monetária da interface de forma consistente com o idioma português brasileiro.
- Criar a tela em `/servicos` e adicionar links para ela nas telas existentes de tutor e pet, sem substituir as rotas atuais.
- Considerar o cadastro confirmado somente se a resposta do Xano contiver `id` e os campos obrigatórios correspondentes ao envio. Caso contrário, exibir erro de confirmação e manter os campos.
- Atualizar `docs/domain-model.md` para incluir o campo conceitual `descricao` em `Servico`, sem alterar o conjunto de entidades.

## Riscos e trade-offs

- A entrada de valores monetários pode usar vírgula no padrão brasileiro; o frontend deve convertê-la corretamente antes de enviar o valor decimal ao Xano.
- Serviços preexistentes com somente campos técnicos podem exigir atenção durante a inclusão dos novos campos no schema.
- A resposta do endpoint precisa retornar o registro persistido para o frontend validar os dados e confirmar sucesso.
