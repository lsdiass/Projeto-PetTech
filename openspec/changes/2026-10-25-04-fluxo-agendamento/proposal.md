# Fluxo de Agendamento

## Por que

O domínio prevê a entidade `Agendamento`, mas a tabela e o endpoint `POST /agendamento` ainda não persistem os dados do atendimento. Sem um fluxo de seleção de Pet, Serviço, data e horário, não é possível agendar com integridade nem evitar sobreposição de horários para o mesmo pet shop.

## O que muda

- Completa o schema de `agendamento` com `pet_id`, `servico_id`, `data_hora`, `status` e `observacoes_atendimento`.
- Implementa no Xano endpoints para consultar disponibilidade e criar um agendamento, validando Pet, Serviço, funcionamento, feriados, horários passados e conflitos por duração.
- Valida os tipos e a presença dos valores temporais antes dos cálculos, usando timestamps diretamente e exigindo duração inteira e positiva.
- Restringe a atualização existente do Agendamento a status e observações, impedindo alterações de Pet, Serviço ou horário que contornem as validações.
- Adiciona no frontend Reflex uma tela de agendamento: seleção de Pet, seleção de Serviço, calendário mensal, escolha de horário e confirmação.
- Exibe horários ocupados desativados e atualiza a disponibilidade após o cadastro.
- Confirma o agendamento somente depois da persistência confirmada pelo Xano.
- Mantém o tutor associado indiretamente pelo Pet, sem duplicar `tutor_id` na tabela `agendamento`.

## Regras de agenda aprovadas

- Agenda global compartilhada pelo pet shop; não há entidade ou seleção de profissionais nesta change.
- Funcionamento de segunda a sábado, das 08:00 às 18:00, sem intervalo de almoço; domingo fechado.
- Horários iniciais oferecidos em incrementos de 30 minutos.
- Cada agendamento ocupa o intervalo completo definido pela duração do Serviço; qualquer sobreposição com outro agendamento ativo torna o horário indisponível.
- Agendamentos cancelados não ocupam horário.
- Não permitir dias ou horários passados.
- Não oferecer horários em feriados nacionais brasileiros; feriados estaduais e municipais ficam fora do escopo enquanto não houver localidade definida.
- Usar o fuso horário `America/Sao_Paulo`.

## Capacidades

### Novas capacidades

- `fluxo-agendamento`: consultar disponibilidade e reservar um horário para um Pet e um Serviço.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: schema da tabela `agendamento` e endpoints no grupo `Event Logs`.
- Frontend: `Petech/Petech.py`.
- OpenSpec: nova especificação para o fluxo de agendamento.
- Não adiciona entidades nem tabelas e mantém o limite de quatro entidades (`Tutor`, `Pet`, `Servico` e `Agendamento`).
