# login-demo Specification

## Purpose

Definir uma tela inicial de login demonstrativo para testar a navegação do Petech sem implementar autenticação real ou proteção de dados.

## Requirements

### Requirement: Apresentar login demonstrativo como página inicial

O sistema MUST apresentar um formulário de login demonstrativo na rota `/`. O formulário MUST aceitar somente as credenciais públicas predefinidas para o protótipo, redirecionar uma combinação válida para `/tutores` e informar erro sem redirecionar para uma combinação inválida.

#### Scenario: Credenciais demonstrativas válidas

- **WHEN** o usuário informa o e-mail e a senha demonstrativos predefinidos
- **THEN** o sistema redireciona o navegador para o cadastro de tutores em `/tutores`

#### Scenario: Credenciais inválidas

- **WHEN** o usuário informa credenciais diferentes das predefinidas
- **THEN** o sistema permanece na página inicial e exibe uma mensagem de erro

### Requirement: Preservar as telas existentes

O cadastro de tutores MUST permanecer acessível em `/tutores`; os cadastros de pets e serviços MUST continuar acessíveis em `/pets` e `/servicos`, respectivamente. Os links entre essas telas MUST apontar para as rotas corretas após a mudança da página inicial.

#### Scenario: Navegação para os cadastros existentes

- **WHEN** o usuário navega entre os cadastros de tutores, pets e serviços
- **THEN** cada link leva à rota correta e os formulários mantêm seu comportamento existente

### Requirement: Identificar o protótipo como não seguro

O sistema MUST informar claramente que o login é demonstrativo e MUST NOT sugerir que rotas, dados ou endpoints estão protegidos. O protótipo MUST NOT criar tokens ou sessões, chamar autenticação no Xano ou impedir acesso direto às rotas existentes.

#### Scenario: Aviso do login demonstrativo

- **WHEN** o usuário acessa a página inicial
- **THEN** a interface informa que as credenciais são públicas e que a tela não implementa proteção real
