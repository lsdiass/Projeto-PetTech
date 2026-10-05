# Modelo de Domínio — Sistema de Gestão para Pet Shop

## 1. Visão Geral do Domínio
O domínio da aplicação engloba o ciclo de vida operacional do atendimento em um pet shop. Ele é delimitado por quatro conceitos fundamentais interconectados: a figura do responsável pelo animal (**Tutor**), o animal atendido (**Pet**), o catálogo comercial do estabelecimento (**Servico**) e a execução/reserva do atendimento (**Agendamento**).

---

## 2. Especificação Detalhada das Entidades

### 2.1. Tutor
- **Descrição:** Representa o cliente final do estabelecimento, responsável financeiramente e legalmente pelos animais cadastrados.
- **Responsabilidade:** Armazenar dados de identificação e contato para comunicação e confirmação de serviços.
- **Atributos Conceituais:**
  - `id`: Identificador único do tutor no sistema.
  - `nome`: Nome completo do cliente.
  - `cpf`: Registro de Pessoa Física para identificação única.
  - `telefone`: Número principal para contato e envio de notificações/confirmações.
  - `email`: Endereço eletrônico para envio de comprovantes e comunicação.
- **Relacionamentos:**
  - Um **Tutor** possui **1 para N** com **Pet** (um tutor pode ter um ou vários pets cadastrados, mas cada pet pertence a exatamente um tutor).

### 2.2. Pet
- **Descrição:** Representa o animal de estimação que receberá os cuidados e serviços prestados pelo pet shop.
- **Responsabilidade:** Manter o perfil físico e o histórico de saúde/comportamento do animal para orientação da equipe técnica.
- **Atributos Conceituais:**
  - `id`: Identificador único do pet no sistema.
  - `tutor_id`: Chave estrangeira que vincula o pet ao seu respectivo Tutor.
  - `nome`: Nome do animal.
  - `especie`: Classificação biológica básica (ex.: Cão, Gato).
  - `raca`: Raça específica do pet (ex.: Poodle, Shih-tzu, Vira-lata / SRD).
  - `porte`: Porte físico do animal (Pequeno, Médio, Grande), utilizado para estimativa do serviço.
  - `observacoes_saude`: Campo descritivo para registrar alergias, problemas dermatológicos, comportamento arisco ou restrições de manuseio.
- **Relacionamentos:**
  - Pertence a um **Tutor** (**N para 1**).
  - Possui **1 para N** com **Agendamento** (um pet pode realizar diversos agendamentos ao longo do tempo).

### 2.3. Servico
- **Descrição:** Representa os itens do catálogo comercial de atendimento oferecidos pelo pet shop.
- **Responsabilidade:** Definir as regras de preço e o tempo padrão necessário para a execução do atendimento.
- **Atributos Conceituais:**
  - `id`: Identificador único do serviço no catálogo.
  - `nome`: Título do serviço (ex.: Banho & Tosa, Tosa Higiênica, Hidratação, Corte de Unha).
  - `preco`: Valor monetário cobrado pela prestação do serviço.
  - `duracao_minutos`: Tempo estimado em minutos para a conclusão do serviço.
- **Relacionamentos:**
  - Possui **1 para N** com **Agendamento** (um mesmo serviço do catálogo pode estar associado a múltiplos agendamentos).

### 2.4. Agendamento
- **Descrição:** Entidade central do sistema que consolida a transação operacional entre o Pet, o Serviço e o Horário marcado.
- **Responsabilidade:** Controlar a agenda, o horário de execução e o status do fluxo de atendimento.
- **Atributos Conceituais:**
  - `id`: Identificador único do agendamento.
  - `pet_id`: Chave estrangeira vinculando o Pet atendido.
  - `servico_id`: Chave estrangeira vinculando o Serviço contratado.
  - `data_hora`: Data e horário exatos programados para o início do atendimento.
  - `status`: Estado atual do atendimento (`Agendado`, `Em Andamento`, `Concluído`, `Cancelado`).
  - `observacoes_atendimento`: Anotações técnicas realizadas pelo profissional durante ou após a prestação do serviço.
- **Relacionamentos:**
  - Associa-se a exatamente um **Pet** (**N para 1**).
  - Associa-se a exatamente um **Servico** (**N para 1**).

---

## 3. Diagrama Conceitual do Domínio

```text
  +---------------+               +---------------+
  |     Tutor     |               |    Servico    |
  +---------------+               +---------------+
  | id            |               | id            |
  | nome          |               | nome          |
  | cpf           |               | preco         |
  | telefone      |               | duracao_min...|
  | email         |               +---------------+
  +-------+-------+                       | 1
          | 1                             |
          |                               |
          | N                             | N
  +-------+-------+               +-------+-------+
  |      Pet      |               |  Agendamento  |
  +---------------+               +---------------+
  | id            | 1           N | id            |
  | tutor_id (FK) +---------------+ pet_id (FK)   |
  | nome          |               | servico_id(FK)|
  | especie       |               | data_hora     |
  | raca          |               | status        |
  | porte         |               | obs_atendim...|
  | obs_saude     |               +---------------+
  +---------------+
  