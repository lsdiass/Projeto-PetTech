# Design

## Contexto

A tabela `agendamento` contém somente `id` e `created_at`, e o `POST /agendamento` atual grava apenas o campo técnico. As entidades Pet e Serviço já têm endpoints de listagem. O modelo de domínio relaciona cada agendamento a exatamente um Pet e um Serviço; o Tutor é determinado pelo tutor responsável daquele Pet.

## Objetivos e não objetivos

**Objetivos:**

- Permitir selecionar um Pet existente e um Serviço existente.
- Apresentar o calendário do mês atual e de meses futuros, sem disponibilizar datas passadas.
- Exibir horários inicializáveis a cada 30 minutos dentro do horário de atendimento.
- Desativar horários cujo intervalo de duração se sobreponha a um agendamento ativo.
- Revalidar todos os dados e conflitos no backend no momento da gravação.
- Salvar o status inicial `Agendado` e confirmar a operação somente após resposta persistida.

**Fora do escopo:**

- Criar entidades, tabelas, profissionais ou recursos de atendimento adicionais.
- Selecionar profissionais ou oferecer agendas independentes por profissional.
- Editar ou excluir agendamentos nesta mudança.
- Implementar cancelamento pela interface; agendamentos cujo status já seja `Cancelado` no backend não ocupam a agenda.
- Definir feriados estaduais ou municipais sem uma localidade configurada.

## Decisões

- A nova tela será acessível em `/agendamentos`, com uma sequência de passos na mesma página: Pet, Serviço, mês/dia, horários e confirmação.
- Carregar Pets por `GET /pet` e Serviços por `GET /servico`; exibir apenas itens com identificador e dados necessários para seleção.
- Consultar os slots do mês em `GET /agendamento_disponibilidade` no Xano, recebendo `servico_id`, `ano` e `mes`. A resposta informa, por dia, os horários iniciais e se cada um está disponível, permitindo desabilitar no calendário datas sem horários livres. O nome sem subcaminho evita colisão com a rota existente `GET /agendamento/{agendamento_id}`.
- A duração é obtida no backend a partir do Serviço selecionado, não confiada a um valor de duração enviado pelo frontend.
- O endpoint recebe `data_hora` como inteiro positivo em milissegundos (epoch), o formato enviado pelo Reflex. A validação de tipo e valor ocorre no input do Xano, e o inteiro validado é usado diretamente em operações aritméticas, sem conversão `to_int` nem coerção implícita de timestamp.
- Em condições que comparam o resultado de um filtro XanoScript, o valor filtrado é delimitado por parênteses antes da comparação para impedir que o filtro consuma o operador subsequente.
- Antes de calcular intervalos, o backend valida que a duração do Serviço existe, é inteira e positiva. A mesma validação é aplicada às durações dos Serviços vinculados a agendamentos existentes, tanto na consulta de disponibilidade quanto na criação.
- Oferecer inícios alinhados à grade de 30 minutos entre 08:00 e 18:00. Só disponibilizar um início quando o horário final calculado pela duração do serviço não ultrapassar 18:00.
- Tratar intervalos como semiabertos `[início, fim)`: um horário candidato conflita quando `início_candidato < fim_existente` e `fim_candidato > início_existente`. Assim, um serviço pode começar exatamente quando o anterior termina.
- Considerar ocupados todos os agendamentos com status diferente de `Cancelado`, em toda a agenda global.
- O endpoint de criação valida que Pet e Serviço existem, que a data não é passada nem domingo/feriado, que o início pertence à grade de 30 minutos, respeita o horário de funcionamento e tem duração disponível, e que não há conflito. O servidor grava `status = "Agendado"`.
- A rota PATCH existente pode atualizar somente `status` e `observacoes_atendimento`; não pode alterar Pet, Serviço ou horário. Status é limitado às etapas do domínio, e um agendamento cancelado não pode ser reativado por essa rota.
- Persistir `pet_id`, `servico_id`, `data_hora` e `status`; o Tutor fica associado por meio de `pet_id` e é obtido a partir do registro de Pet, sem campo duplicado na tabela de agendamento.
- Usar `America/Sao_Paulo` para interpretar datas e horas da agenda.
- A confirmação do frontend exige resposta com identificador e Pet, Serviço, data/hora e status correspondentes. Em caso de erro ou falta de confirmação, preservar os dados para nova tentativa.
- Exibir confirmação textual `Agendado com sucesso!` e atualizar os horários exibidos após criação confirmada.
- Impedir submissões repetidas enquanto uma confirmação está em andamento. Em respostas HTTP 429 ou 5xx, manter as seleções sem disparar uma nova consulta de disponibilidade; em 429, orientar o usuário a aguardar o período informado pelo `Retry-After`, quando disponível.
- Identificar feriados nacionais brasileiros no backend como dias sem horários disponíveis; não incluir feriados locais nesta change.

## Riscos e trade-offs

- Uma consulta de disponibilidade pode ficar desatualizada antes da confirmação; por isso, o endpoint de criação precisa recalcular a disponibilidade e rejeitar o conflito, mesmo quando a interface mostrou o horário como livre.
- A criação revalida conflitos e insere dentro de `db.transaction`. A documentação do Xano descreve atomicidade da transação, mas não garante isolamento serializável nem bloqueio do intervalo; requisições concorrentes podem ainda observar a mesma vaga livre. A change não declara proteção absoluta contra essa corrida. Uma garantia forte exige mecanismo de serialização/bloqueio que deve ser validado antes de uso em produção.
- O calendário de feriados requer uma regra confiável no backend para feriados nacionais fixos e móveis. Feriados estaduais, municipais e fechamentos extraordinários não são cobertos.
- A rota de atualização mantém cancelamentos e anotações, mas não oferece reativação de um registro cancelado; um novo atendimento deve ser agendado em outra reserva.
- A regra é global porque o modelo atual não possui profissionais ou recursos de agenda independentes; isso limita atendimentos simultâneos a intervalos sem sobreposição.
