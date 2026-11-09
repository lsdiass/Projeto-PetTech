# Login do Cliente como Página Inicial

## Por que

Ao abrir a aplicação, a rota inicial exibe o login administrativo demonstrativo.
O fluxo principal para os clientes deve começar diretamente no login da área do
Tutor.

## O que muda

- Define o login do cliente como a página da rota raiz (`/`).
- Mantém `/cliente` como rota alternativa compatível para o mesmo login.
- Disponibiliza o login administrativo em `/admin/login`.
- Atualiza os links entre os acessos do cliente e administrativo.

## Impacto

- Reflex: ajusta o registro de páginas e os links de navegação.
- Não altera autenticação, backend, entidades ou regras de negócio.
