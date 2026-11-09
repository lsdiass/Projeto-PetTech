# Tarefas: Cadastro e Acesso de Clientes

## Backend (Xano)

- [x] **T-BK-00**: Conferir os dados existentes no Xano antes de aplicar os índices únicos; os registros encontrados não tinham e-mails duplicados.
- [x] **T-BK-01**: Habilitar autenticação na tabela `tutor`, incluir CPF e senha e definir índices únicos para CPF e e-mail no script local.
- [x] **T-BK-02**: Criar endpoint local de cadastro que valide os dados obrigatórios, CPF, unicidade e senha e retorne apenas dados seguros.
- [x] **T-BK-03**: Criar endpoint local de login que valide credenciais e emita token Xano sem revelar se e-mail ou senha estavam incorretos.
- [x] **T-BK-04**: Criar endpoint autenticado de perfil e projetar campos seguros nas respostas de Tutor existentes.
- [x] **T-BK-05**: Validar sintaticamente todos os scripts Xano alterados.
- [x] **T-BK-06**: Publicar os scripts no workspace Xano e validar rotas, proteção do perfil, rejeição de CPF inválido e credenciais inexistentes sem criar conta.
- [ ] **T-BK-07**: Validar criação e login completos com uma conta de teste autorizada; pendente para evitar inserir um registro de teste persistente sem necessidade ou autorização específica.

## Frontend (Reflex)

- [x] **T-FT-01**: Adicionar acesso de cliente à página inicial sem alterar o login demonstrativo do administrador.
- [x] **T-FT-02**: Criar formulário de conta de Tutor com nome, CPF, telefone, e-mail, senha e confirmação.
- [x] **T-FT-03**: Criar login de cliente integrado ao Xano, com mensagens de erro explícitas e estado privado do token.
- [x] **T-FT-04**: Criar a página inicial autenticada do cliente, validar sessão no Xano e oferecer saída.
- [x] **T-FT-05**: Validar compilação Reflex e simular cadastro/login válidos, confirmação divergente, perfil, sessão expirada, credenciais inválidas e erro de conexão.

## Especificações

- [x] **T-SPEC-01**: Atualizar os requisitos de navegação do login demonstrativo para apontar ao novo acesso de cliente.
- [x] **T-SPEC-02**: Ajustar o escopo do cadastro administrativo de Tutor para coexistir com os campos de autenticação.
