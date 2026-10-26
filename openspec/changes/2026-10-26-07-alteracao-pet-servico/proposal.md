# Alteração de Pet e Serviço

## Por que

As telas de Pet e Serviço permitem cadastrar registros, mas não oferecem uma forma de corrigir ou atualizar dados já persistidos.

## O que muda

- Lista pets cadastrados em `/pets` e permite editar tutor, nome, espécie, raça, porte e observações.
- Lista serviços cadastrados em `/servicos` e permite editar nome, descrição, preço e duração.
- Mantém visíveis registros legados que tenham identificador, mas estejam sem dados obrigatórios, sinalizando-os para correção pela edição.
- Valida os dados e a existência dos registros e do tutor no Xano antes da atualização.
- Confirma a alteração no frontend somente quando a resposta corresponder aos dados enviados.
- Mantém o cadastro atual e não oferece exclusão.

## Capacidades

### Novas capacidades

- `alteracao-pet-servico`: consulta e alteração de pets e serviços existentes.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: `PATCH /pet/{pet_id}` e `PATCH /servico/{servico_id}` no grupo `Event Logs`.
- Frontend: telas e estados em `Petech/Petech.py`.
- OpenSpec: nova especificação de alteração de Pet e Serviço.
- Não adiciona tabelas nem entidades ao domínio.
