# Design

## Contexto

O dashboard do Tutor já consulta seu perfil, Pets e Agendamentos por meio de
`GET /cliente/sessao/dashboard`. O cadastro administrativo de Pet permite nome,
espécie, raça opcional, porte e observações opcionais. O fluxo operacional de
Agendamento oferece Serviços do catálogo, disponibilidade mensal e confirmação
com regras de expediente, feriados e conflito de duração. Os endpoints
administrativos existentes são globais e não devem ser usados para gravar dados
em nome de uma conta de cliente.

## Objetivos e não objetivos

**Objetivos:**

- Permitir cadastrar um ou vários Pets autenticados no Tutor da sessão, sem
  aceitar `tutor_id` do navegador.
- Oferecer a ação de criar Agendamento tanto quando a lista de ativos está
  vazia quanto quando já existem Agendamentos ativos.
- Vincular Agendamento a um Pet comprovadamente pertencente ao Tutor e a um
  Serviço existente.
- Revalidar disponibilidade e conflitos no Xano antes da gravação.
- Atualizar o dashboard após confirmação e preservar dados digitados em falhas.
- Manter o histórico apenas informativo e mostrar estado vazio quando não houver
  registros históricos.

**Fora do escopo:**

- Editar ou excluir Pets pelo dashboard.
- Cancelar, editar ou excluir Agendamentos pelo dashboard.
- Adicionar entidades, tabelas ou novos status.
- Alterar fluxos e permissões das telas administrativas.
- Aceitar cadastro de Agendamento por endpoint público sem validar o Tutor.

## Decisões

- Criar endpoints autenticados `POST /cliente/sessao/pets` e
  `POST /cliente/sessao/agendamentos`, sem colisão com as rotas dinâmicas
  administrativas `/pet/{id}` e `/agendamento/{id}`.
- O endpoint de Pet deriva `tutor_id` de `$auth.id`, valida nome e espécie
  obrigatórios e limita porte a Pequeno, Médio ou Grande. Raça e observações de
  saúde/comportamento são opcionais.
- O endpoint de Agendamento exige que o Pet exista e tenha
  `pet.tutor_id == $auth.id`; Serviço e duração são validados no backend. Deve
  repetir as regras do endpoint administrativo de criação: data futura,
  horário entre 08:00 e 18:00 em grade de 30 minutos, encerramento até 18:00,
  dias úteis, feriados nacionais, duração positiva e ausência de sobreposição
  com qualquer Agendamento não cancelado. A criação e revalidação ficam em
  transação; isso não implica isolamento serializável.
- O dashboard oferece um formulário expansível na seção Pets e permite cadastrar
  outro mesmo havendo Pets existentes. Após confirmação, recarrega o dashboard.
- A ação “Agendar atendimento” aparece na seção de ativos independentemente de
  existirem Agendamentos ativos. O formulário permite selecionar somente Pets
  do dashboard, carregar Serviços do catálogo e selecionar dia/horário
  disponível pela API mensal existente.
- A confirmação exige identificador, Pet, Serviço, data/hora e status
  correspondentes ao envio. O sucesso atualiza o dashboard e a disponibilidade;
  erros mantêm o formulário aberto com seleções intactas.
- A seção de histórico permanece somente leitura. Erros de carregamento são
  distintos de lista vazia.
- As ações de cadastro e agendamento utilizam o token privado já guardado no
  estado Reflex. Token ausente ou rejeitado não pode gravar dados.

## Riscos e trade-offs

- O endpoint de Agendamento autenticado compartilha as regras operacionais do
  endpoint administrativo; mudanças futuras na regra de agenda devem manter os
  dois comportamentos consistentes.
- Disponibilidade pode mudar entre consulta e gravação; a verificação de
  conflitos no endpoint autenticado reduz a janela, mas não garante
  serialização de requisições concorrentes.
- O histórico pode crescer sem paginação, comportamento já existente no
  dashboard e fora do escopo desta extensão.
