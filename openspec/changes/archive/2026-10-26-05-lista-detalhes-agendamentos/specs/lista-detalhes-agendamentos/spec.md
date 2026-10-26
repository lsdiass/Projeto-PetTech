# lista-detalhes-agendamentos Specification

## Purpose

Permitir consultar agendamentos salvos e visualizar os dados relacionados de Tutor, Pet, Serviço, data/hora e status.

## Requirements

### Requirement: Listar agendamentos salvos

O sistema MUST oferecer uma página de consulta que carregue registros do endpoint `GET /agendamento` e apresente uma lista selecionável. Falhas HTTP, de conexão ou respostas incompatíveis MUST ser comunicadas sem aparentar que a lista foi carregada com sucesso.

#### Scenario: Existem agendamentos

- **WHEN** as listas de Agendamento, Pet, Serviço e Tutor retornam respostas válidas
- **THEN** a página apresenta os agendamentos retornados, associados às entidades relacionadas pelos identificadores existentes

#### Scenario: Não existem agendamentos

- **WHEN** o endpoint retorna uma lista vazia
- **THEN** a página informa que não há agendamentos cadastrados

#### Scenario: Falha ao carregar

- **WHEN** uma requisição falha ou retorna estrutura incompatível
- **THEN** a página informa qual carregamento falhou e não apresenta os dados como confirmados

### Requirement: Exibir detalhes e vínculos

Cada agendamento selecionável MUST permitir visualizar Tutor, Pet, Serviço, data/hora formatada e Status. O Tutor MUST ser resolvido pelo vínculo `pet.tutor_id`. A data/hora em epoch de milissegundos MUST ser formatada no fuso `America/Sao_Paulo`.

#### Scenario: Abrir detalhes

- **WHEN** o usuário seleciona um item válido da lista
- **THEN** o painel de detalhes exibe Tutor, Pet, Serviço, data/hora local e Status daquele agendamento

#### Scenario: Referência não encontrada

- **WHEN** um identificador de Tutor, Pet ou Serviço não corresponde à lista relacionada
- **THEN** o detalhe identifica explicitamente a referência ausente sem omitir o agendamento silenciosamente
