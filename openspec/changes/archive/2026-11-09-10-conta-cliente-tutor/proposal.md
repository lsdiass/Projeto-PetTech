# Cadastro e Acesso de Clientes

## Por que

O PetTech possui apenas uma tela de acesso demonstrativa, com credenciais fixas
validadas localmente. Tutores ainda não podem criar credenciais nem entrar em
uma área própria.

## O que muda

- Adiciona uma opção de acesso do cliente separada do login demonstrativo do
  administrador.
- Permite que um novo Tutor crie uma conta com nome, CPF, telefone, e-mail e
  senha.
- Permite que o Tutor entre com e-mail e senha e acesse uma página inicial da
  área do cliente.
- Usa o Xano para validar credenciais e armazenar a senha com hash.
- Mantém o domínio limitado às quatro entidades existentes, habilitando
  autenticação na tabela `tutor`.
- Preserva o aviso de que o login administrativo atual é somente demonstrativo.

## Capacidades

### Novas capacidades

- `conta-cliente-tutor`: cadastro, autenticação e acesso inicial do Tutor.

### Capacidades modificadas

- `login-demo`: oferece navegação para o acesso de clientes sem alterar o
  comportamento demonstrativo do login administrativo.

## Impacto

- Xano: tabela `tutor` e endpoints do grupo `Event Logs` para cadastro,
  autenticação e consulta autenticada da conta.
- Frontend Reflex: tela de entrada, formulário de cadastro, login de cliente e
  página inicial autenticada.
- OpenSpec: nova capacidade de conta de cliente e ajuste da navegação do login.
- Não cria tabelas nem altera Pet, Serviço ou Agendamento.
