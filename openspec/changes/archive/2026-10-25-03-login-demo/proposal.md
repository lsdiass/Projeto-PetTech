# Tela Inicial de Login Demonstrativo

## Por que

Ao iniciar o Petech, o usuário chega diretamente ao cadastro de tutor. Uma tela inicial de login demonstrativo estabelece uma entrada clara para a aplicação e permite testar o fluxo de acesso antes da implementação de autenticação real.

## O que muda

- Substitui a página inicial `/` por um formulário de login demonstrativo.
- Adiciona credenciais públicas e predefinidas para testar o fluxo da tela.
- Redireciona credenciais válidas para o cadastro de tutores em `/tutores` e informa erro para credenciais inválidas.
- Mantém disponíveis as telas existentes de tutores, pets e serviços com navegação entre elas.
- Informa explicitamente na interface que o protótipo não implementa autenticação real nem protege rotas ou dados.

## Capacidades

### Novas capacidades

- `login-demo`: fluxo visual de login demonstrativo como página inicial do Petech.

### Capacidades modificadas

- Nenhuma.

## Impacto

- Frontend: `Petech/Petech.py`.
- OpenSpec: nova especificação do protótipo de login.
- Não altera o backend Xano, não cria entidades e não adiciona autenticação ou autorização.
