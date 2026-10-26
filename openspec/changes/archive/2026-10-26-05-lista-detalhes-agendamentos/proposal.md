# Lista e detalhes de agendamentos

## Por que

O sistema permite criar agendamentos, mas não oferece uma tela para consultar os registros salvos e seus vínculos de Tutor, Pet e Serviço.

## O que muda

- Adiciona a rota Reflex `/agendamentos/lista`.
- Carrega agendamentos pelo endpoint `GET /agendamento` e resolve os vínculos consultando as listas existentes de Pet, Serviço e Tutor.
- Exibe os registros em uma lista e apresenta os dados completos do item selecionado em um painel de detalhes.
- Formata o timestamp de milissegundos no fuso `America/Sao_Paulo`.

## Escopo

- Não altera tabelas, endpoints ou regras de negócio do Xano.
- Não adiciona entidades nem campos persistidos.
