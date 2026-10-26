# Design

## Decisões

- A nova tela usa a rota `/agendamentos/lista`, sem conflitar com o fluxo de criação existente em `/agendamentos`.
- A leitura usa `GET /agendamento`, `GET /pet`, `GET /servico` e `GET /tutor`, todos já existentes. As chamadas são sequenciais para não gerar um pico simultâneo de requisições.
- O estado Reflex associa registros por ID em memória. O Tutor é resolvido por `pet.tutor_id`, sem duplicar o vínculo no Agendamento.
- A data/hora retornada como epoch em milissegundos é convertida para `America/Sao_Paulo` e exibida em formato local.
- A seleção abre um painel de detalhes na própria página; não é necessário novo componente ou dependência de modal.
- Erros HTTP e respostas com estrutura inválida são informados explicitamente. Referências ausentes são identificadas no detalhe em vez de ocultadas.

## Fora do escopo

- Alterar API, banco, status ou regras do Agendamento.
- Paginação, busca, edição, cancelamento ou exclusão.
