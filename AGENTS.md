<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** � up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above � do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs � components, state management, events, styling, database, routing, authentication � use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available � always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

# Instruções para Agentes de IA

## Regras de Trabalho e Conduta
1. **Consulta Obrigatória de Contexto:** Antes de planejar, propor ou alterar qualquer código/estrutura, consulte os arquivos de documentação do projeto localizados em `docs/project-overview.md` e `docs/domain-model.md`.
2. **Uso do OpenSpec:** Todas as alterações funcionais e arquiteturais devem seguir estritamente o fluxo do OpenSpec.
3. **Escopo Restrito (4 Entidades):** O banco de dados e a regra de negócio do projeto são estritamente limitados às 4 entidades definidas (`Tutor`, `Pet`, `Servico`, `Agendamento`). Não adicione novas tabelas ou módulos secundários (como estoque ou permissões complexas) sem autorização expressa.
4. **Backend em Xano:** Todas as validações, regras de negócio e controle de integridade dos dados devem ser implementadas no Backend (Xano / XanoScript).
5. **Modificações Pontuais:** Não altere arquivos ou funcionalidades que não estejam diretamente relacionados à tarefa/change atual.
