# Especificação: Login do Cliente como Página Inicial

## Requisito: Abrir o login do cliente na rota inicial

A aplicação MUST exibir o login do cliente quando acessada pela rota `/`.
O login administrativo demonstrativo MUST permanecer acessível em
`/admin/login`, e a rota `/cliente` MUST continuar exibindo o login do cliente.

### Cenário: Acesso inicial à aplicação

- **WHEN** o usuário abre a rota `/`
- **THEN** a aplicação exibe o login da área do cliente

### Cenário: Acesso administrativo

- **WHEN** o usuário abre `/admin/login`
- **THEN** a aplicação exibe o login administrativo demonstrativo

### Cenário: Compatibilidade do login do cliente

- **WHEN** o usuário abre `/cliente`
- **THEN** a aplicação exibe o login da área do cliente

### Cenário: Navegação entre acessos

- **WHEN** o usuário está em uma tela de login
- **THEN** a tela oferece o acesso correspondente à outra área sem alterar as
  rotas de cadastro ou dashboard do cliente
