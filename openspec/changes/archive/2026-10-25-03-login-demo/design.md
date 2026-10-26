# Design

## Contexto

A rota `/` atualmente apresenta o cadastro de tutor. O app já registra telas de cadastro de pets em `/pets` e serviços em `/servicos`; a tela de tutor pode ser movida para `/tutores` sem alterar seu comportamento de persistência.

O escopo aprovado é um protótipo de demonstração, não uma funcionalidade de autenticação. As credenciais predefinidas são públicas e não podem ser consideradas secretas.

## Objetivos e não objetivos

**Objetivos:**

- Apresentar o formulário de login como a primeira tela na rota `/`.
- Permitir testar o envio de credenciais demonstrativas válidas e inválidas.
- Preservar o acesso às páginas de cadastro existentes após mover o cadastro de tutor para `/tutores`.
- Deixar visível que o protótipo não fornece proteção de segurança.

**Fora do escopo:**

- Autenticar usuários no Xano ou validar identidade real.
- Criar tabela, entidade, sessão, cookie, token, middleware ou controle de acesso.
- Proteger as rotas de tutor, pets e serviços ou endpoints da API.
- Adicionar cadastro, recuperação de senha ou gerenciamento de usuários.

## Decisões

- Registrar a página demonstrativa em `/` e mover o cadastro de tutor para `/tutores`.
- Validar a combinação de e-mail e senha demonstrativos no estado Reflex e redirecionar credenciais válidas para `/tutores`.
- Exibir uma mensagem de erro sem redirecionar para credenciais incorretas.
- Informar as credenciais públicas demonstrativas na própria interface para que possam ser testadas, sem apresentá-las como segredo.
- Mostrar um aviso claro de que o login é apenas demonstrativo e não protege rotas ou dados.
- Atualizar os links de retorno existentes para apontar ao cadastro de tutor em `/tutores`; manter os cadastros de pets e serviços acessíveis por suas rotas atuais.

## Riscos e trade-offs

- Qualquer visitante pode consultar as credenciais e acessar diretamente as rotas de cadastro; esse é o comportamento previsto para o protótipo e não deve ser usado como controle de acesso.
- Uma futura implementação de autenticação real deverá substituir este fluxo por validação no backend e proteção efetiva das rotas.
