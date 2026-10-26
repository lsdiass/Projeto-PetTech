# Alteração de Tutor

## Por que

O sistema permite cadastrar tutores, mas não oferece uma forma de corrigir os dados de um tutor já persistido. Isso impede a manutenção dos dados de identificação e contato quando eles mudam ou são cadastrados incorretamente.

## O que muda

- Permite consultar os tutores cadastrados na tela `/tutores` e iniciar a edição de um registro.
- Permite alterar nome, e-mail e telefone, preservando o cadastro existente e os demais registros.
- Valida no Xano o identificador, o nome, o e-mail opcional e a existência do tutor antes de atualizar.
- Confirma a alteração no frontend somente quando a resposta do Xano contém o mesmo tutor e os dados enviados.

## Capacidades

### Novas capacidades

- `alteracao-tutor`: consulta e alteração dos dados de tutores existentes.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Xano: endpoints `GET /tutor` e `PATCH /tutor/{tutor_id}` do grupo `Event Logs`.
- Frontend: tela e estado de tutor em `Petech/Petech.py`.
- OpenSpec: nova especificação de alteração de Tutor.
- Não adiciona entidades ou tabelas e não altera Pet, Serviço ou Agendamento.
