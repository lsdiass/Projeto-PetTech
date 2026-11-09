# conta-cliente-tutor Specification

## Purpose

Definir a criação e o acesso seguro de contas de Tutor usando a entidade
existente e o backend Xano.

## Requirements

### Requirement: Separar acesso administrativo demonstrativo e acesso do cliente

A rota `/` MUST preservar o login demonstrativo atual e MUST oferecer uma
navegação explícita para `/cliente`. A tela de cliente MUST permitir entrar com
credenciais existentes e acessar o cadastro de nova conta. O login
administrativo MUST continuar identificado como demonstrativo e MUST NOT ser
apresentado como autenticação real.

#### Scenario: Abrir acesso de cliente

- **WHEN** o usuário seleciona o acesso do cliente na página inicial
- **THEN** o sistema abre a tela `/cliente` sem alterar as credenciais ou o
  destino do login demonstrativo

#### Scenario: Abrir cadastro de cliente

- **WHEN** o usuário ainda não possui uma conta e escolhe criar uma
- **THEN** o sistema abre o formulário `/cliente/cadastro`

### Requirement: Criar conta de Tutor

A tela `/cliente/cadastro` MUST solicitar nome, CPF, telefone, e-mail, senha e
confirmação de senha. O frontend MUST exigir confirmação coincidente antes do
envio. O Xano MUST validar campos obrigatórios, formato de CPF e e-mail,
comprimento mínimo da senha e unicidade do CPF e do e-mail antes de gravar o
Tutor. A senha MUST ser persistida somente como hash pelo tipo `password` do
Xano. A resposta MUST conter somente identificador, nome, e-mail e token de
autenticação, sem senha ou hash.

#### Scenario: Criar conta com dados válidos

- **WHEN** o novo Tutor envia dados válidos e confirma a própria senha
- **THEN** o Xano grava uma conta de Tutor com senha protegida por hash
- **AND** retorna um token e os dados públicos necessários
- **AND** o frontend abre `/cliente/inicio`

#### Scenario: Rejeitar dados inválidos ou duplicados

- **WHEN** o cadastro contém dados obrigatórios inválidos, CPF inválido,
  senha abaixo do mínimo ou CPF/e-mail já cadastrado
- **THEN** o Xano rejeita o cadastro sem criar outra conta
- **AND** o frontend apresenta o erro sem indicar sucesso

#### Scenario: Senhas de confirmação diferentes

- **WHEN** a confirmação não corresponde à senha informada
- **THEN** o frontend não envia o cadastro e solicita que as senhas sejam
  corrigidas

### Requirement: Autenticar o Tutor no Xano

A tela `/cliente` MUST enviar e-mail e senha ao Xano. O backend MUST comparar a
senha com o hash armazenado, emitir token somente para credenciais válidas e
responder com erro genérico para credenciais inválidas. O token MUST permanecer
em estado privado no servidor Reflex e MUST NOT ser renderizado ou sincronizado
com o navegador. O login administrativo demonstrativo MUST permanecer separado.

#### Scenario: Entrar com credenciais válidas

- **WHEN** um Tutor cadastrado envia e-mail e senha corretos
- **THEN** o Xano valida as credenciais e emite token
- **AND** o frontend guarda o token em estado privado e abre `/cliente/inicio`

#### Scenario: Entrar com credenciais inválidas

- **WHEN** um usuário envia e-mail ou senha inválidos
- **THEN** o Xano não emite token e retorna erro genérico
- **AND** a tela de cliente exibe uma mensagem de falha sem revelar qual campo
  estava incorreto

#### Scenario: Falha de comunicação

- **WHEN** o Xano está indisponível ou retorna resposta inválida
- **THEN** o frontend informa que não foi possível autenticar e não abre a área
  autenticada

### Requirement: Restringir e encerrar a sessão de cliente

A página `/cliente/inicio` MUST validar o token por `GET
/cliente/sessao/perfil`, endpoint Xano autenticado, e exibir somente a
identificação pública do Tutor. Sem token válido, MUST
redirecionar para `/cliente`. A ação de sair MUST limpar o token privado e
retornar à tela de login. Os endpoints de cadastro, login, listagem, leitura e
edição de Tutor MUST NOT retornar senha ou hash de senha.

#### Scenario: Abrir área autenticada com sessão válida

- **WHEN** um Tutor autenticado acessa `/cliente/inicio`
- **THEN** o Xano confirma a sessão e a página apresenta o nome do Tutor

#### Scenario: Abrir área sem sessão válida

- **WHEN** um usuário acessa `/cliente/inicio` sem token ou com token inválido
- **THEN** o acesso é recusado e o usuário retorna para `/cliente`

#### Scenario: Indisponibilidade ao validar sessão

- **WHEN** o frontend não consegue confirmar a sessão junto ao Xano
- **THEN** a área autenticada não exibe dados do Tutor
- **AND** o usuário retorna para `/cliente` com uma mensagem de erro

#### Scenario: Sair da conta

- **WHEN** o Tutor seleciona sair
- **THEN** o token é removido do estado privado e a tela `/cliente` é exibida

#### Scenario: Proteger senha e hash nas respostas

- **WHEN** qualquer endpoint de Tutor retorna dados ao frontend
- **THEN** a resposta não contém senha nem hash de senha
