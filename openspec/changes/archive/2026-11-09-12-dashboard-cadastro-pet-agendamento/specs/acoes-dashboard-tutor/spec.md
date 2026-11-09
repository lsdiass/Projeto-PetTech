# acoes-dashboard-tutor Specification

## Purpose

Definir o cadastro autenticado de Pets e o agendamento de novos atendimentos
pela área do Tutor, mantendo a propriedade e as regras de agenda no Xano.

## Requirements

### Requirement: Cadastrar Pets vinculados ao Tutor autenticado

A seção “Seus Pets” MUST oferecer cadastro quando não houver Pets e uma ação de
cadastrar outro quando já houver. O formulário MUST aceitar nome e espécie
obrigatórios, porte Pequeno/Médio/Grande, raça opcional e observações de saúde
ou comportamento opcionais. O endpoint Xano MUST exigir autenticação de Tutor,
definir o `tutor_id` usando `$auth.id` e MUST NOT aceitar vínculo informado pelo
cliente. Após resposta persistida correspondente, o dashboard MUST exibir o
novo Pet.

#### Scenario: Cadastrar primeiro Pet

- **WHEN** o Tutor autenticado ainda não possui Pets e envia os campos válidos
- **THEN** o Xano cria o Pet para o Tutor autenticado
- **AND** o dashboard apresenta o Pet após confirmação

#### Scenario: Cadastrar Pet adicional

- **WHEN** o Tutor já possui pelo menos um Pet e cadastra outro com dados válidos
- **THEN** o novo Pet é criado e todos os Pets do Tutor permanecem visíveis

#### Scenario: Rejeitar dados inválidos ou vínculo de outra conta

- **WHEN** campos obrigatórios ou porte são inválidos, ou o cliente tenta enviar
  `tutor_id` arbitrário
- **THEN** o backend rejeita a gravação ou ignora qualquer vínculo informado
- **AND** nenhum Pet é criado para outro Tutor

#### Scenario: Falha no cadastro

- **WHEN** o Xano falha, rejeita a sessão ou retorna resposta incompleta
- **THEN** a interface informa o erro sem confirmar sucesso e preserva os campos
  preenchidos

#### Scenario: Autenticação do cadastro de Pet

- **WHEN** o Tutor possui uma sessão válida e envia o cadastro de um Pet
- **THEN** a interface envia o token da sessão no cabeçalho `Authorization`
  usando o esquema `Bearer`
- **AND** o Xano aceita a autenticação e processa o cadastro para o Tutor logado

### Requirement: Criar Agendamento para Pet próprio

A seção de Agendamentos ativos MUST oferecer a ação de criar um Agendamento
quando vazia e quando já houver registros ativos. A interface MUST permitir
selecionar somente Pets do Tutor autenticado, um Serviço do catálogo, uma data e
um horário retornados como disponíveis. O endpoint Xano MUST exigir
autenticação, verificar que o Pet pertence a `$auth.id`, validar o Serviço e
revalidar as regras de disponibilidade e conflito no backend antes de criar um
Agendamento com status inicial `Agendado`.

#### Scenario: Criar Agendamento com Pet próprio

- **WHEN** o Tutor escolhe um Pet seu, Serviço e horário disponível e confirma
- **THEN** o Xano persiste um Agendamento vinculado ao Pet e Serviço com status
  `Agendado`
- **AND** o dashboard apresenta a confirmação e atualiza os dados

#### Scenario: Tutor sem Pet tenta agendar

- **WHEN** o Tutor não possui Pets cadastrados
- **THEN** a interface orienta o cadastro do primeiro Pet e não permite
  confirmar um Agendamento

#### Scenario: Pet de outro Tutor

- **WHEN** uma requisição autenticada tenta agendar um Pet pertencente a outro
  Tutor
- **THEN** o Xano rejeita a requisição sem criar Agendamento

#### Scenario: Serviço, data ou conflito inválido

- **WHEN** o Serviço não existe, o horário deixou de estar disponível ou viola
  expediente, grade, data, feriado, duração ou conflito
- **THEN** o Xano rejeita a criação sem persistir um Agendamento
- **AND** a interface apresenta o erro sem mostrar sucesso e preserva as escolhas

#### Scenario: Falha na confirmação

- **WHEN** a conexão falha, o Xano rejeita ou a resposta não confirma os campos
  persistidos
- **THEN** o dashboard não mostra sucesso e mantém o formulário e seleções para
  nova tentativa

### Requirement: Manter histórico de Agendamentos

A seção “Histórico de Agendamentos” MUST continuar apresentando registros
`Concluído` e `Cancelado` do Tutor autenticado, sem ações de alteração nesta
mudança. Quando não houver registros, MUST exibir o estado vazio; falhas de
carregamento MUST ser exibidas como erro, não como histórico vazio.

#### Scenario: Exibir histórico existente

- **WHEN** o Tutor possui Agendamentos concluídos ou cancelados
- **THEN** o dashboard mostra seus registros com Pet, Serviço, data/hora e status

#### Scenario: Histórico vazio

- **WHEN** o Tutor não possui Agendamentos históricos
- **THEN** a seção informa que ainda não há histórico
