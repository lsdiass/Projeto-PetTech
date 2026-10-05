# Project Overview — Sistema Web para Gestão e Agendamento em Pet Shops

## 1. Visão Geral do Projeto
O presente projeto consiste no desenvolvimento de uma aplicação web voltada para a gestão operacional e automação de agendamentos de serviços em micro e pequenos pet shops. A solução busca centralizar as informações de tutores, animais de estimação, catálogo de serviços e controle de horários em uma única plataforma web intuitiva e eficiente. O sistema foi projetado para resolver os principais gargalos operacionais no atendimento ao cliente, otimizando o tempo da equipe e melhorando a qualidade do serviço prestado através do acompanhamento do histórico de cada animal.

## 2. Contexto e Problematização
O mercado de pet shops e serviços veterinários no Brasil apresenta crescimento expressivo. Contudo, a grande maioria dos micro e pequenos estabelecimentos ainda opera utilizando métodos arcaicos de gestão operacional, como cadernos físicos, planilhas descentralizadas e trocas de mensagens informais via aplicativos de conversa (como o WhatsApp). 

Essa ausência de padronização gera diversos impactos negativos diretos na sustentabilidade e lucratividade do negócio:
- **Conflito e Erros de Agendamento:** Marcações duplas no mesmo horário para o mesmo profissional ou para a mesma estrutura física (banheiras e mesas de tosa).
- **Ociosidade e Prejuízo por No-Show:** Falhas de confirmação e esquecimento por parte dos clientes levam a faltas não notificadas, deixando profissionais ociosos e reduzindo o faturamento diário.
- **Perda de Histórico Operacional:** Inexistência de um registro centralizado sobre particularidades do pet (ex.: tipo de tosa preferida, alergias a produtos específicos, comportamento arisco, restrições médicas). Isso obriga o tutor a repor as mesmas instruções em toda visita, aumentando o risco de falhas no atendimento.
- **Ineficiência Operacional:** Gasto excessivo de tempo dos colaboradores na confirmação manual e gestão de horários, desviando o foco da atividade-fim do estabelecimento.

## 3. Objetivos
### 3.1. Objetivo Geral
Desenvolver e implementar uma aplicação web centralizada de gestão para micro e pequenos pet shops, com foco na automação do fluxo de agendamentos e no rastreamento do histórico de atendimento dos pets.

### 3.2. Objetivos Específicos
- Mapear os gargalos operacionais e o fluxo de trabalho típico de agendamento em pet shops de pequeno porte.
- Modelar e estruturar um banco de dados relacional enxuto e normalizado, composto por exatamente 4 entidades operacionais.
- Implementar uma interface web focada na experiência do usuário (UX), permitindo a visualização da agenda diária/semanal e o acompanhamento do status do serviço em tempo real.
- Centralizar os registros de preferências e condições de saúde dos pets para garantir um atendimento personalizado e seguro.

## 4. Público-Alvo e Perfis de Usuário
O sistema destina-se a estabelecimentos de pequeno porte e possui os seguintes perfis de uso:
- **Atendentes e Recepcionistas:** Responsáveis por cadastrar tutores, registrar pets, agendar atendimentos e gerenciar a fila do dia.
- **Tosadores e Banhistas:** Profissionais operacionais que consultam a lista de serviços do dia, verificam as observações técnicas de cada animal (ex.: cuidados especiais, tipo de shampoo) e atualizam o status da execução.
- **Gestores/Proprietários:** Acompanham o volume diário de atendimentos e gerenciam o catálogo de serviços prestados e seus respectivos valores.

## 5. Escopo e Funcionalidades Principais

### 5.1. Módulo de Gestão de Clientes e Pets
- **Cadastro e Manutenção de Tutores:** Registro completo dos dados de contato do cliente (nome, CPF, telefone e e-mail).
- **Ficha do Pet:** Vincular animais ao tutor responsável, registrando dados essenciais como nome, espécie, raça, porte e campo dedicado a observações médicas e comportamentais.

### 5.2. Módulo de Gestão de Serviços
- **Catálogo de Serviços:** Cadastro e controle do portfólio do estabelecimento (ex.: Banho, Tosa Higiênica, Tosa da Raça, Corte de Unhas, Hidratação), contendo preço e tempo médio estimado de execução.

### 5.3. Módulo de Agendamento e Controle Operacional
- **Central de Agendamento:** Registro de marcações vinculando obrigatoriamente um Pet, um Serviço e uma Data/Hora específica.
- **Gestão do Ciclo de Vida do Atendimento:** Acompanhamento do status de cada serviço por meio das etapas: `Agendado`, `Em Andamento`, `Concluído` e `Cancelado`.
- **Histórico de Atendimentos:** Consulta ao histórico retroativo de todos os serviços realizados por determinado pet.

## 6. Arquitetura e Restrições Tecnológicas
- **Backend e Persistência:** Plataforma Xano, responsável pelo banco de dados relacional (Xano DB) e pela lógica de negócio via XanoScript.
- **Regras de Negócio e Validações:** Centralizadas integralmente no Backend para assegurar integridade dos dados e segurança.
- **Interface e Ferramentas de Desenvolvimento:** Editor VS Code, controle de versão via Git/GitHub e metodologia OpenSpec orientada a especificações.
- **Restrição Estrita de Modelo:** O banco de dados do projeto é limitado formalmente a 4 entidades funcionais para manter a objetividade acadêmica e o escopo exequível.

## 7. Critérios de Sucesso do Projeto
- **Integridade Operacional:** Impedir a criação de agendamentos inconsistentes ou orfãos.
- **Usabilidade:** Permitir que o operador conclua um novo agendamento em poucos cliques a partir do dashboard.
- **Disponibilidade dos Dados:** Garantir que as observações de saúde e histórico do pet estejam acessíveis na tela de atendimento imediato.