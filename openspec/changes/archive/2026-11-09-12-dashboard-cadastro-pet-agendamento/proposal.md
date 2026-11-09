# Cadastro de Pet e Agendamento no Dashboard do Tutor

## Por que

O dashboard informa quando o Tutor ainda não possui Pets ou Agendamentos, mas
não permite realizar essas ações na área autenticada do cliente. O Tutor deve
poder cadastrar Pets sob sua própria conta e reservar novos atendimentos sem
depender das telas operacionais administrativas.

## O que muda

- Permite cadastrar Pets diretamente na seção “Seus Pets”, usando os campos do
  cadastro existente e vinculando o registro ao Tutor autenticado no Xano.
- Permite iniciar um novo Agendamento na seção de ativos, esteja ela vazia ou
  já contenha Agendamentos.
- O fluxo de Agendamento usa os Pets do Tutor, Serviços do catálogo, calendário
  de disponibilidade existente e confirmação de gravação no backend.
- A seção de histórico continua exibindo Agendamentos concluídos e cancelados;
  quando vazia, informa que não há histórico.
- Mantém os endpoints e as telas administrativas existentes.

## Capacidades

### Novas capacidades

- `acoes-dashboard-tutor`: cadastro de Pet e criação segura de Agendamento pelo
  Tutor autenticado.

### Capacidades modificadas

- `dashboard-cliente`: oferece ações de cadastro e reserva integradas às seções
  de Pets e Agendamentos.

## Impacto

- Xano: endpoints de criação autenticados para Pet e Agendamento, sem adicionar
  tabelas ou entidades.
- Reflex: formulário de Pet, seleção de Serviço/Pet e fluxo de calendário no
  dashboard.
- Documentação do escopo de clientes.
