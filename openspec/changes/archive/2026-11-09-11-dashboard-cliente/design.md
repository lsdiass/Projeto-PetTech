# Design

## Contexto

A área do cliente já autentica Tutores pelo Xano. A página `/cliente/inicio`
atualmente mostra somente o nome do usuário e a ação de sair. As entidades
Pet e Agendamento relacionam os Pets e atendimentos ao Tutor, e o projeto deve
permanecer limitado às quatro entidades existentes.

## Objetivos e não objetivos

**Objetivos:**

- Apresentar os dados cadastrais do Tutor da sessão atual.
- Exibir somente os Pets cujo `tutor_id` corresponde ao Tutor autenticado.
- Exibir Agendamentos associados a esses Pets, separados em ativos e histórico.
- Manter senha e dados de outros Tutores fora da resposta.
- Informar falhas de carregamento sem apresentar listas parciais como completas.

**Fora do escopo:**

- Alterar dados cadastrais ou dados de Pets.
- Criar, editar ou cancelar Agendamentos pelo dashboard.
- Adicionar tabelas, endpoints de domínio ou novas entidades.
- Mostrar Pets, dados pessoais ou Agendamentos de outros Tutores.

## Decisões

- Manter a rota `/cliente/inicio` e atualizar o endpoint autenticado para
  `GET /cliente/sessao/dashboard`.
- O Xano obtém o Tutor por `$auth.id`, consulta Pets por `tutor_id == $auth.id`
  e consulta Agendamentos com join ao Pet, também exigindo
  `pet.tutor_id == $auth.id`. O Serviço é unido para retornar somente seu nome.
- Retornar campos explicitamente projetados: dados cadastrais sem senha, dados
  descritivos dos Pets e informações de exibição dos Agendamentos.
- Considerar `Agendado` e `Em Andamento` ativos; considerar `Concluído` e
  `Cancelado` histórico. O backend retorna status do domínio e o Reflex divide
  as listas após validar o formato da resposta.
- Ordenar Agendamentos por `data_hora` decrescente para priorizar os próximos
  atendimentos na seção de ativos e mostrar os registros recentes no histórico.
- Formatar datas no fuso `America/Sao_Paulo`, usando o helper existente.
- Exibir estado vazio distinto para ausência de Pets ou de Agendamentos e manter
  visível o erro quando a consulta falhar.
- Manter a ação de sair no dashboard e não alterar os endpoints administrativos.

## Riscos e trade-offs

- A junção usa chaves existentes; Agendamentos com referências inválidas não
  aparecem, pois o join é interno. Isso é preferível a revelar referências ou
  dados de outras contas.
- A leitura agregada pode ficar maior conforme cresce o histórico; paginação
  fica fora do escopo inicial.
- A implantação requer publicar o novo endpoint no workspace Xano.
