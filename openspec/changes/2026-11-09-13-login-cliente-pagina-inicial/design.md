# Design: Login do Cliente como Página Inicial

## Decisão

Registrar `cliente_login` na rota `/` e manter sua rota atual `/cliente`.
Mover a página de login demonstrativo (`login`) de `/` para `/admin/login`.

## Navegação

- A página do cliente aponta para `/admin/login` quando o usuário precisa do
  acesso administrativo.
- A página administrativa aponta para `/` para retornar ao acesso principal
  do cliente.

## Compatibilidade

Rotas já usadas pelo cadastro e dashboard do cliente permanecem inalteradas.
`/cliente` continua disponível como endereço alternativo para o login do Tutor.
