# Cadastro de Tutor

## Why

Os cadastros precisam ser persistidos na tabela de tutores do Xano. O endpoint antigo no grupo `PetTech` respondia sucesso sem gravar dados, enquanto o endpoint funcional pertence ao grupo `Event Logs`.

## What Changes

- Define o schema da tabela `tutor` com nome obrigatório e e-mail e telefone opcionais.
- Implementa validação de entrada e gravação no endpoint `POST /tutor` do grupo `Event Logs`.
- Cria o formulário Reflex e integra o envio ao endpoint correto.
- Só confirma sucesso no frontend quando o Xano retorna o identificador do tutor persistido.
- Remove arquivos legados do Xano que referenciavam tabelas fora do domínio Petech.

## Capabilities

### New Capabilities
- `cadastro-tutor`: cadastro, validação e confirmação de persistência de tutores.

### Modified Capabilities
- Nenhuma.

## Impact

- Xano: tabela `tutor` e endpoint `POST /tutor` no grupo `Event Logs`.
- Frontend: `Petech/Petech.py`.
- Limpeza dos arquivos legados em `xano/`; sem adicionar entidades ao modelo de domínio.
