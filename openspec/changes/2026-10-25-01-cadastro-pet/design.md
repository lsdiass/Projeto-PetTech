# Design

## Contexto

A tabela `pet` contém somente os campos técnicos `id` e `created_at`, e o endpoint `POST /pet` não recebe nem grava dados de domínio. O endpoint existente `GET /tutor` já retorna os tutores cadastrados e pode alimentar a seleção do responsável no formulário.

O frontend atual apresenta apenas o cadastro de tutores na rota principal. A implementação do novo formulário deve preservar esse fluxo e oferecer acesso entre as duas telas.

## Objetivos e não objetivos

**Objetivos:**

- Persistir a ficha do pet e sua referência obrigatória ao tutor.
- Validar no Xano a existência do tutor e os dados obrigatórios antes da gravação.
- Permitir selecionar um tutor já cadastrado no formulário.
- Dar feedback de sucesso somente após confirmação de persistência pelo identificador retornado.

**Fora do escopo:**

- Criar entidades, tabelas ou módulos adicionais.
- Alterar o cadastro de tutor ou os endpoints GET existentes.
- Adicionar edição, exclusão, listagem de pets ou agendamentos nesta mudança.

## Decisões

- Manter os campos de Pet definidos no modelo de domínio: `tutor_id`, `nome`, `especie`, `raca`, `porte` e `observacoes_saude`.
- Tornar obrigatórios `tutor_id`, `nome`, `especie` e `porte`; manter `raca` e `observacoes_saude` opcionais.
- Restringir `porte` aos valores `Pequeno`, `Médio` e `Grande`, conforme o modelo de domínio.
- Validar no backend que `tutor_id` corresponde a um tutor existente antes de criar o pet.
- Obter as opções de tutor pelo endpoint `GET /tutor` do grupo `Event Logs`. Se o carregamento falhar ou não houver tutores cadastrados, informar o problema e não permitir um envio sem responsável válido.
- Adicionar a tela em `/pets` e links entre ela e a tela atual de cadastro de tutores, preservando a rota principal.
- Tratar sucesso somente se a resposta de `POST /pet` contiver o `id` do registro persistido. Falhas HTTP, de conexão ou respostas sem identificador devem manter os dados preenchidos e exibir erro.

## Riscos e trade-offs

- A lista de tutores depende da disponibilidade e do formato de resposta do endpoint existente `GET /tutor`.
- A validação do tutor no backend é necessária mesmo com a seleção no frontend, pois dados enviados pelo cliente não garantem a integridade do relacionamento.
- A inclusão de campos no schema deve ser compatível com os registros de Pet já existentes, que atualmente contêm apenas os campos técnicos.
