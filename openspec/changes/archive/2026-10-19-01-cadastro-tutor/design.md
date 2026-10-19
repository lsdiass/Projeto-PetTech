# Design

## Context

O Xano expõe mais de um grupo com um caminho `POST /tutor`. O grupo `PetTech` contém um endpoint sem lógica de persistência; o grupo `Event Logs` contém o endpoint que valida os dados e grava na tabela `tutor`. O frontend Reflex faz a chamada pelo servidor, usando `httpx`.

## Goals / Non-Goals

**Goals:**
- Encaminhar os cadastros ao endpoint de `Event Logs`.
- Evitar confirmação de sucesso sem o identificador retornado pelo Xano.
- Manter o domínio restrito às quatro entidades existentes.

**Non-Goals:**
- Criar autenticação ou entidades adicionais.
- Alterar ou excluir endpoints remotos que não fazem parte desta correção.
- Criar um registro de tutor artificial apenas para teste.

## Decisions

- Fixar o URL base do grupo `Event Logs` usado pelo workspace Petech para impedir que uma variável antiga redirecione o formulário para o endpoint sem persistência.
- Enviar apenas campos opcionais preenchidos e deixar o backend validar o e-mail e gravar o registro.
- Tratar a resposta como sucesso somente quando for um objeto de tutor contendo `id`; erros HTTP, rede ou JSON inválido permanecem erros visíveis.
- Preservar `T-BK-03` e `T-FT-05` como tarefas de teste do endpoint e do fluxo, sem criar dados reais no workspace durante a verificação.

## Risks / Trade-offs

- O endpoint remoto continua dependente do workspace e grupo Xano configurados para o ambiente Petech; uma mudança de workspace exige atualizar a URL.
- A confirmação do frontend depende do endpoint retornar o objeto persistido com o campo `id`.
