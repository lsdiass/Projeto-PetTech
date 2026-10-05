# Instruções para Agentes de IA

## Regras de Trabalho e Conduta
1. **Consulta Obrigatória de Contexto:** Antes de planejar, propor ou alterar qualquer código/estrutura, consulte os arquivos de documentação do projeto localizados em `docs/project-overview.md` e `docs/domain-model.md`.
2. **Uso do OpenSpec:** Todas as alterações funcionais e arquiteturais devem seguir estritamente o fluxo do OpenSpec.
3. **Escopo Restrito (4 Entidades):** O banco de dados e a regra de negócio do projeto são estritamente limitados às 4 entidades definidas (`Tutor`, `Pet`, `Servico`, `Agendamento`). Não adicione novas tabelas ou módulos secundários (como estoque ou permissões complexas) sem autorização expressa.
4. **Backend em Xano:** Todas as validações, regras de negócio e controle de integridade dos dados devem ser implementadas no Backend (Xano / XanoScript).
5. **Modificações Pontuais:** Não altere arquivos ou funcionalidades que não estejam diretamente relacionados à tarefa/change atual.