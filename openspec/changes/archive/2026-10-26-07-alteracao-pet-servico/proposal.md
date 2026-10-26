# Alteração de Pet e Serviço

## Por que

As telas de Pet e Serviço permitem cadastrar registros, mas precisam permitir corrigir os dados de registros já persistidos.

## O que muda

- Lista pets cadastrados em `/pets` e permite editar tutor, nome, espécie, raça, porte e observações.
- Lista serviços cadastrados em `/servicos` e permite editar nome, descrição, preço e duração.
- Mantém visíveis registros legados com identificador válido e campos obrigatórios incompletos, sinalizando-os para correção.
- Valida os dados e a existência dos registros e do tutor no Xano antes da atualização.
- Confirma alterações no frontend somente quando a resposta corresponde aos dados enviados.
- Mantém os fluxos de cadastro e não oferece exclusão nesta change.

## Capacidades

### Novas capacidades

- `alteracao-pet-servico`: consulta e alteração de pets e serviços existentes.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: `GET /pet`, `GET /servico`, `PATCH /pet/{pet_id}` e `PATCH /servico/{servico_id}` do grupo `Event Logs`.
- Frontend: telas e estados em `Petech/Petech.py`.
- OpenSpec: requisitos de alteração e correção de registros legados incompletos.
- Não adiciona entidades ou tabelas.
