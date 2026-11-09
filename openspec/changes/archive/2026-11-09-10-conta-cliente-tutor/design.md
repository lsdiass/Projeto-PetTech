# Design

## Contexto

O login da rota `/` usa credenciais públicas fixas e não implementa
autenticação. A tabela `tutor` ainda não tem CPF nem credenciais. O projeto
restringe o domínio a quatro entidades e centraliza validação e integridade no
Xano.

## Objetivos e não objetivos

**Objetivos:**

- Separar a entrada demonstrativa do administrador do acesso do cliente.
- Criar uma conta de Tutor validada e persistida pelo Xano.
- Verificar a senha exclusivamente no backend e nunca armazená-la em texto
  puro.
- Manter as quatro entidades existentes e evitar expor hashes de senha nas
  respostas atuais de Tutor.
- Permitir que um cliente autenticado chegue a uma página inicial própria e
  encerre a sessão.

**Fora do escopo:**

- Converter o login demonstrativo em autenticação real de administrador.
- Proteger ou remodelar os endpoints administrativos existentes.
- Implementar redefinição de senha, confirmação de e-mail ou gestão de papéis.
- Adicionar funcionalidades de agendamento ou cadastro de Pets na área do
  cliente.
- Adicionar tabelas ou módulos fora de Tutor, Pet, Servico e Agendamento.

## Decisões

- Manter `/` como entrada demonstrativa do administrador e incluir um link
  explícito para `/cliente`.
- Usar `/cliente` para login do Tutor, `/cliente/cadastro` para criação da conta
  e `/cliente/inicio` para a página inicial autenticada.
- Habilitar `auth = true` na tabela `tutor`, adicionar CPF e senha, e marcar
  senha e dados pessoais como sensíveis. O campo de senha usa o tipo `password`
  do Xano, que aplica hash automaticamente.
- Permitir que o cadastro administrativo legado continue sem senha; apenas
  registros com e-mail e senha válidos conseguem autenticar. O cadastro de
  conta exige CPF, telefone, e-mail e senha.
- O Xano verifica formato e unicidade do e-mail e CPF, valida os campos
  obrigatórios e gera o token de autenticação. O cliente Reflex não decide a
  validade da conta.
- Guardar o token apenas em variável privada de estado do Reflex, que não é
  sincronizada com o navegador. A consulta da conta usa
  `/cliente/sessao/perfil`, com prefixo estático adicional para evitar colisão
  com uma rota legada dinâmica `/cliente/{cliente_id}`. A página inicial
  revalida o token no backend e redireciona para o login em caso de sessão
  inválida.
- Respostas existentes de listagem, leitura e edição de Tutor devem projetar
  somente os campos necessários e nunca retornar senha ou hash.
- Após cadastro ou login bem-sucedido, redirecionar para `/cliente/inicio`.
  Essa página apresenta apenas a identificação do Tutor e a ação de sair, sem
  introduzir funcionalidades fora do pedido.

## Riscos e trade-offs

- Tutores cadastrados anteriormente sem senha precisarão criar credenciais por
  um fluxo futuro antes de conseguir usar o login do cliente.
- CPF passa a ser dado sensível e deve permanecer ausente de respostas que não
  precisem dele.
- Os arquivos XanoScript locais precisam ser sincronizados e publicados no
  workspace Xano para que os endpoints remotos fiquem disponíveis.
- Índices únicos novos podem exigir tratamento de CPFs ou e-mails duplicados
  que já existam na tabela antes da migração.
- O login administrativo permanece demonstrativo e não protege as rotas
  administrativas existentes.
