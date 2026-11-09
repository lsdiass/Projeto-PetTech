# dashboard-cliente Specification

## Purpose

Definir a consulta e a apresentação dos dados cadastrais, Pets e Agendamentos
do Tutor autenticado, sem expor dados pertencentes a outras contas.

## Requirements

### Requirement: Exibir dados cadastrais do Tutor autenticado

A página `/cliente/inicio` MUST apresentar nome, CPF, telefone e e-mail do Tutor
retornado por endpoint autenticado do Xano. A resposta MUST corresponder ao ID
da sessão autenticada e MUST NOT incluir senha ou hash.

#### Scenario: Carregar perfil da sessão atual

- **WHEN** o Tutor acessa o dashboard com token válido
- **THEN** a interface exibe os dados cadastrais retornados para seu próprio ID
- **AND** não exibe senha nem hash

### Requirement: Listar Pets do Tutor autenticado

O Xano MUST consultar somente Pets cujo `tutor_id` corresponde a `$auth.id`. A
interface MUST apresentar nome, espécie, raça e porte, distinguindo lista vazia
de erro de carregamento.

#### Scenario: Tutor possui Pets

- **WHEN** o Tutor autenticado possui Pets cadastrados
- **THEN** o dashboard apresenta somente os Pets vinculados à sua conta

#### Scenario: Tutor não possui Pets

- **WHEN** o Tutor autenticado não possui Pets
- **THEN** o dashboard informa que ainda não há Pets cadastrados

### Requirement: Separar Agendamentos ativos e histórico

O Xano MUST retornar somente Agendamentos relacionados a Pets cujo `tutor_id`
corresponde a `$auth.id`, junto ao nome do Pet e do Serviço. A interface MUST
classificar `Agendado` e `Em Andamento` como ativos, e `Concluído` e `Cancelado`
como histórico. Cada registro MUST exibir Pet, Serviço, data/hora e status. As
datas MUST ser apresentadas no fuso `America/Sao_Paulo`.

#### Scenario: Tutor possui Agendamentos em ambas as categorias

- **WHEN** existem Agendamentos dos quatro status associados aos Pets do Tutor
- **THEN** Agendado e Em Andamento aparecem na seção de ativos
- **AND** Concluído e Cancelado aparecem na seção de histórico

#### Scenario: Não há Agendamentos de uma categoria

- **WHEN** não há registros ativos ou não há registros históricos para o Tutor
- **THEN** a seção correspondente informa que não há Agendamentos nessa categoria

#### Scenario: Proteger Agendamentos de outros Tutores

- **WHEN** o endpoint é requisitado com token válido de um Tutor
- **THEN** nenhum Agendamento associado somente a Pets de outro Tutor aparece

### Requirement: Tratar falhas e preservar sessão

O dashboard MUST validar o token antes de exibir dados. Uma sessão inválida MUST
redirecionar para `/cliente`. Falhas de conexão, HTTP ou resposta incompleta MUST
serem apresentadas como erro e MUST NOT ser representadas como listas vazias ou
como carregamento bem-sucedido. A ação de sair MUST continuar disponível.

#### Scenario: Sessão inválida

- **WHEN** o Xano rejeita o token do Tutor
- **THEN** o dashboard não exibe dados e o usuário retorna para `/cliente`

#### Scenario: Falha ao carregar o dashboard

- **WHEN** o endpoint falha ou retorna dados malformados
- **THEN** a interface exibe uma mensagem de erro e não apresenta listas parciais
  como resultado completo

#### Scenario: Sair do dashboard

- **WHEN** o Tutor seleciona sair
- **THEN** o token é removido do estado privado e o usuário retorna para `/cliente`
