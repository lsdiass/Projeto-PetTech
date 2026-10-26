# fluxo-agendamento Specification

## Purpose

Definir a consulta de disponibilidade e a criação de agendamentos para Pets e Serviços existentes, evitando sobreposição de intervalos e confirmando sucesso somente após persistência.

## Requirements

### Requirement: Selecionar Pet e Serviço existentes

O fluxo MUST exigir a seleção de exatamente um Pet existente e um Serviço existente antes de apresentar horários. O Agendamento MUST ser vinculado a `pet_id` e `servico_id`. O Tutor responsável MUST ser obtido do Pet selecionado, sem duplicar `tutor_id` no Agendamento.

#### Scenario: Seleções válidas

- **WHEN** o usuário seleciona um Pet e um Serviço retornados pelos endpoints de listagem
- **THEN** o fluxo apresenta o calendário e usa a duração do Serviço selecionado para consultar a disponibilidade

#### Scenario: Pet ou Serviço indisponível

- **WHEN** as listas de Pet ou Serviço não carregam, estão vazias ou não contêm registros válidos
- **THEN** o fluxo informa a situação e impede a criação de um Agendamento incompleto

### Requirement: Exibir dias agendáveis no calendário

O sistema MUST apresentar o mês atual e meses futuros no fuso `America/Sao_Paulo`. MUST impedir a seleção de datas passadas, domingos, feriados nacionais brasileiros e dias sem nenhum horário possível para a duração do Serviço selecionado. O backend MUST aplicar as mesmas regras independentemente do estado da interface.

#### Scenario: Dia com disponibilidade

- **WHEN** um dia não passado, de segunda a sábado, dentro do período permitido, possui ao menos um horário disponível para o Serviço
- **THEN** o calendário permite selecionar o dia

#### Scenario: Data não agendável

- **WHEN** a data selecionada é passada, domingo, feriado nacional ou não possui início possível dentro do expediente para a duração do Serviço
- **THEN** o sistema não oferece horários para a data e o backend rejeita uma tentativa direta de criação

### Requirement: Calcular horários disponíveis por duração e conflito

O estabelecimento funciona de segunda a sábado, das 08:00 às 18:00, sem intervalo de almoço, e permanece fechado aos domingos e feriados nacionais brasileiros. O sistema MUST oferecer horários iniciais alinhados em incrementos de 30 minutos. Um início só pode ser reservado quando o término calculado a partir da duração persistida do Serviço não ultrapassa 18:00 e não se sobrepõe a nenhum Agendamento cujo status seja diferente de `Cancelado`.

Os intervalos MUST ser comparados como semiabertos `[início, fim)`: existe conflito se `início_candidato < fim_existente` e `fim_candidato > início_existente`. A consulta de disponibilidade e a criação MUST aplicar a regra no backend.

#### Scenario: Intervalo livre

- **WHEN** um horário inicial pertence à grade de 30 minutos, o Serviço termina até 18:00 e o intervalo não se sobrepõe a Agendamento não cancelado
- **THEN** o horário é retornado como disponível e pode ser selecionado

#### Scenario: Sobreposição com agendamento ativo

- **WHEN** o intervalo candidato se sobrepõe a um Agendamento cujo status não é `Cancelado`
- **THEN** o horário é retornado como indisponível, aparece desativado na interface e o backend rejeita a criação

#### Scenario: Limite do expediente

- **WHEN** a duração do Serviço faria o Agendamento terminar depois das 18:00
- **THEN** o horário não é oferecido e uma tentativa de criação é rejeitada

#### Scenario: Agendamento cancelado

- **WHEN** o único intervalo sobreposto pertence a um Agendamento com status `Cancelado`
- **THEN** esse Agendamento não ocupa o intervalo e o horário pode ser oferecido se as demais regras permitirem

### Requirement: Criar Agendamento com integridade no backend

O endpoint `POST /agendamento` MUST validar a existência do Pet e do Serviço, obter a duração do Serviço no backend e revalidar data, horário de funcionamento, feriado, alinhamento e conflitos antes de gravar. O sistema MUST persistir `pet_id`, `servico_id`, `data_hora` e status inicial `Agendado`; o tutor do agendamento é o tutor associado ao Pet. O backend MUST rejeitar qualquer entrada inválida sem criar registro.

Antes de qualquer cálculo temporal, o backend MUST exigir `data_hora` como inteiro positivo em milissegundos (epoch) e rejeitar entradas ausentes ou fora desse tipo. O backend MUST rejeitar duração ausente, não inteira ou não positiva para o Serviço selecionado e para Serviços vinculados a agendamentos existentes. O inteiro de `data_hora` MUST ser usado diretamente em cálculos, sem conversão `to_int` nem coerção implícita de timestamp.

#### Scenario: Cadastro confirmado

- **WHEN** o cliente envia Pet, Serviço e data/hora disponíveis e válidos
- **THEN** o Xano persiste o Agendamento com status `Agendado` e retorna o registro com identificador

#### Scenario: Referência inexistente

- **WHEN** o cliente envia um identificador de Pet ou Serviço que não existe
- **THEN** o Xano rejeita a entrada e não cria um Agendamento

#### Scenario: Data ou duração inválida

- **WHEN** o cliente omite `data_hora`, envia valor que não seja um inteiro positivo em milissegundos ou o Serviço não possui uma duração inteira e positiva
- **THEN** o Xano rejeita a entrada antes de qualquer cálculo temporal e não cria um Agendamento

#### Scenario: Horário deixou de estar disponível

- **WHEN** outro Agendamento ocupa o intervalo antes da confirmação da reserva
- **THEN** o Xano rejeita a criação sem persistir um Agendamento sobreposto

### Requirement: Confirmar somente agendamentos persistidos

O frontend MUST exibir `Agendado com sucesso!` e limpar as seleções somente após receber um Agendamento persistido com `id`, `pet_id`, `servico_id`, `data_hora` e status `Agendado` correspondentes ao envio. Falhas HTTP, de conexão, respostas inválidas, sem identificador ou divergentes MUST ser informadas sem mostrar sucesso. Após sucesso, os horários MUST ser atualizados.

#### Scenario: Persistência confirmada

- **WHEN** o endpoint retorna o Agendamento persistido com identificador e dados esperados
- **THEN** a interface exibe `Agendado com sucesso!` e atualiza a disponibilidade do dia

#### Scenario: Conflito ou falha no envio

- **WHEN** o backend rejeita o horário por conflito, a conexão falha ou a resposta não confirma os dados persistidos
- **THEN** a interface informa que o agendamento não foi confirmado, mantém as seleções e atualiza a disponibilidade quando aplicável

#### Scenario: Limite de requisições do backend

- **WHEN** o Xano responde HTTP 429 ao criar um Agendamento
- **THEN** o sistema mantém as seleções, informa que as chamadas foram limitadas e orienta a aguardar o valor de `Retry-After` quando fornecido, sem consultar novamente a disponibilidade automaticamente

#### Scenario: Evitar submissões repetidas

- **WHEN** uma confirmação está em andamento
- **THEN** o sistema impede o envio de outra confirmação até a primeira terminar

### Requirement: Preservar integridade nas atualizações de Agendamento

A rota de atualização de Agendamento MUST permitir somente alterações de `status` e `observacoes_atendimento`. MUST rejeitar alterações de `pet_id`, `servico_id` ou `data_hora` por essa rota. Um Agendamento com status `Cancelado` MUST NOT ser reativado.

#### Scenario: Atualizar status ou observações

- **WHEN** o cliente atualiza um status válido ou as observações de atendimento de um Agendamento existente
- **THEN** o Xano altera somente os campos permitidos e mantém o vínculo e o horário originais

#### Scenario: Tentar alterar o horário ou reativar cancelamento

- **WHEN** o cliente tenta modificar Pet, Serviço ou data/hora, ou reativar um Agendamento cancelado
- **THEN** o Xano rejeita a operação sem alterar o Agendamento
