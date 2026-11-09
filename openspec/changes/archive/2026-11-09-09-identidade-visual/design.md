# Design

## Contexto

O PetTech possui fluxos de autenticação, cadastros, agenda e listas operacionais.
A atualização deve unificar sua apresentação sem introduzir alterações
funcionais ou mudanças no domínio restrito a Tutor, Pet, Servico e Agendamento.

## Objetivos e não objetivos

**Objetivos:**

- Adotar uma aparência clara, acolhedora e profissional em todas as páginas.
- Padronizar cores, tipografia, cartões, botões, campos e estados de foco.
- Preservar conteúdo, navegação e comportamento dos fluxos existentes.
- Registrar as decisões visuais para orientar a manutenção da interface.

**Fora do escopo:**

- Alterar páginas, rotas, conteúdo, ações ou regras de negócio.
- Modificar o backend Xano ou o modelo de dados.
- Adicionar componentes ou funcionalidades operacionais.

## Decisões

- Usar o verde sálvia como cor primária e o pêssego como acento, sobre fundo
  creme e superfícies claras, conforme `docs/ui-style-guide.md`.
- Definir Poppins para títulos e Nunito Sans para corpo e controles.
- Configurar o tema global do Reflex com aparência clara e aplicar estilos
  compartilhados por meio de `assets/pettech.css`.
- Aplicar a classe `pettech-card` aos cartões existentes selecionados, com
  borda, cantos arredondados e sombra discreta; manter os demais elementos e
  estruturas sem mudanças funcionais.
- Manter foco de teclado visível e ajustar o raio dos cartões em telas pequenas.
- Não incluir imagens, novas rotas, dependências de backend ou mudanças de
  persistência.

## Riscos e trade-offs

- As fontes são carregadas de um provedor externo; indisponibilidade pode fazer
  a interface usar fontes alternativas do navegador.
- A aparência de componentes depende dos estilos globais e do tema do Reflex;
  futuras páginas devem seguir o guia para preservar consistência.
