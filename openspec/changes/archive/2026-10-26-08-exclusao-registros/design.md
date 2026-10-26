# Design

## Contexto

O sistema possui Tutores, Pets, Serviços e Agendamentos. Pets dependem de Tutor, e Agendamentos mantêm referências a Pet e Serviço. As interfaces permitem excluir registros mediante confirmação, e o backend precisa preservar essas relações e o histórico operacional.

## Objetivos e não objetivos

**Objetivos:**

- Permitir exclusão de Tutor, Pet e Serviço com confirmação explícita.
- Bloquear no backend a exclusão de registros que possuam dependências.
- Confirmar remoção no frontend somente após resposta confiável do Xano.
- Preservar registros e informar erro ou incerteza quando a exclusão não for comprovada.

**Fora do escopo:**

- Excluir Agendamentos ou criar remoção em cascata.
- Transferir Pets para outro Tutor automaticamente.
- Adicionar entidades, tabelas ou módulos ao domínio.
- Alterar operações de cadastro, edição ou regras de Agendamento.

## Decisões

- Usar confirmação em dois passos nas listas: iniciar exclusão não envia DELETE; o usuário pode confirmar ou cancelar.
- No Xano, validar identificador positivo e existência antes da exclusão.
- Rejeitar Tutor com Pet vinculado, Pet com Agendamento vinculado e Serviço com Agendamento vinculado. Para Pet e Serviço, todos os Agendamentos, inclusive cancelados, preservam o histórico e bloqueiam a exclusão.
- Nunca excluir registros relacionados em cascata.
- Retornar `{id, deleted: true}` após exclusão confirmada.
- Remover o item da lista quando a resposta confirmar o identificador e `deleted: true`. Se o DELETE retornar sucesso sem confirmação reconhecível, consultar o GET individual e considerar excluído somente com resposta 404.
- Em erro HTTP, mostrar a mensagem do Xano ou o status HTTP se não houver mensagem; em falha de conexão, verificação inconclusiva ou registro ainda existente, manter o item na lista e informar que não foi possível confirmar a exclusão.
- O backend é a autoridade de integridade; o frontend não decide se existem dependências.

## Riscos e trade-offs

- A verificação de dependências ocorre antes da exclusão; integridade sob concorrência depende das garantias transacionais e de chave estrangeira do workspace Xano.
- Registros ligados a histórico permanecem cadastrados até existir um fluxo próprio para tratar seus vínculos.
- Uma falha de rede após o DELETE pode deixar o resultado incerto; a consulta GET individual reduz essa incerteza sem presumir sucesso.
