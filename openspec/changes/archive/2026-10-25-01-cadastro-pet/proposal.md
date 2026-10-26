# Cadastro de Pet

## Por que

O domínio já define Pet como um animal vinculado a exatamente um Tutor, mas a tabela e o endpoint `POST /pet` ainda não persistem os dados do animal nem validam esse relacionamento. Sem isso, não é possível manter uma ficha útil do pet ou garantir que ele tenha um responsável cadastrado.

## O que muda

- Completa o schema da tabela `pet` com `tutor_id`, `nome`, `especie`, `raca`, `porte` e `observacoes_saude`.
- Implementa no endpoint `POST /pet` a validação dos campos obrigatórios, dos valores de porte e da existência do tutor informado.
- Adiciona no frontend Reflex uma tela de cadastro de pets em `/pets`, com seleção de tutor carregada pelo endpoint existente `GET /tutor`.
- Adiciona navegação entre o cadastro atual de tutores e o novo cadastro de pets.
- Confirma o cadastro somente quando o Xano retornar o identificador do pet persistido.

## Capacidades

### Novas capacidades

- `cadastro-pet`: cadastro de pets com vínculo obrigatório a um tutor existente.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: schema de `pet` e endpoint `POST /pet` no grupo `Event Logs`.
- Frontend: `Petech/Petech.py`.
- OpenSpec: nova especificação para cadastro de pets.
- Não adiciona entidades, tabelas ou módulos fora do domínio existente.
