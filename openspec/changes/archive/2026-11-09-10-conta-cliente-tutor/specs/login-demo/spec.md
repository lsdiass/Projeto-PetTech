## MODIFIED Requirements

### Requirement: Apresentar login demonstrativo como página inicial

O sistema MUST apresentar um formulário de login demonstrativo na rota `/`. O
formulário MUST aceitar somente as credenciais públicas predefinidas para o
protótipo, redirecionar uma combinação válida para `/tutores` e informar erro
sem redirecionar para uma combinação inválida. A página MUST oferecer uma
navegação identificada para o acesso do cliente em `/cliente`, sem alterar o
comportamento demonstrativo nem sugerir que o acesso administrativo é
autenticado.

#### Scenario: Credenciais demonstrativas válidas

- **WHEN** o usuário informa o e-mail e a senha demonstrativos predefinidos
- **THEN** o sistema redireciona o navegador para o cadastro de tutores em
  `/tutores`

#### Scenario: Credenciais inválidas

- **WHEN** o usuário informa credenciais diferentes das predefinidas
- **THEN** o sistema permanece na página inicial e exibe uma mensagem de erro

#### Scenario: Acessar a área de cliente

- **WHEN** o usuário seleciona o acesso do cliente na página inicial
- **THEN** o sistema navega para `/cliente` e mantém o login administrativo
  demonstrativo separado
