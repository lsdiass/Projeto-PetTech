# Identidade visual e guia de interface — PetTech

Este guia define a camada visual da interface do PetTech. A proposta combina
acolhimento e tranquilidade com uma aparência profissional e clara para o uso
diário em um pet shop.

## Paleta de cores

| Token | HEX | Aplicação | Tom emocional |
|---|---|---|---|
| Primária — verde sálvia | `#52796F` | Ações principais, links e identidade | Natural, confiável e tranquilizador |
| Primária escura | `#3E6259` | Hover de ações e ênfase | Seguro e estável |
| Secundária — pêssego | `#E7906D` | Destaques, pequenos acentos e foco | Afetuoso, otimista e convidativo |
| Secundária escura | `#CF7653` | Hover de elementos pêssego | Quente e enérgico |
| Fundo — creme | `#FBF8F3` | Fundo geral das páginas | Leve, confortável e menos frio que branco puro |
| Superfície — branco | `#FFFFFF` | Formulários, cards e áreas elevadas | Limpo e organizado |
| Texto principal — carvão esverdeado | `#26352F` | Títulos e conteúdo de maior prioridade | Sério, legível e conectado à paleta |
| Texto secundário — cinza sálvia | `#718078` | Apoio, metadados e instruções | Discreto sem parecer rígido |
| Bordas — areia clara | `#E7E1D8` | Contornos de cards e separadores | Suave e acolhedor |

Use a primária para ações cotidianas. Reserve o pêssego para destacar uma ação
prioritária ou um detalhe; não use as duas cores saturadas em grandes áreas.
Para mensagens de status, preserve contraste e use cores semânticas distintas
da identidade quando apropriado.

## Tipografia

- **Títulos:** [Poppins](https://fonts.google.com/specimen/Poppins), pesos
  500–700. Formas geométricas e arredondadas dão personalidade sem perder
  profissionalismo.
- **Corpo e controles:** [Nunito Sans](https://fonts.google.com/specimen/Nunito+Sans),
  pesos 400–800. Tem leitura confortável, desenho amigável e boa distinção em
  formulários.
- Use títulos com peso 600 e espaçamento levemente compacto. Mantenha textos de
  interface em frases curtas e com altura de linha entre 1.5 e 1.65.
- Evite usar caixa alta em frases inteiras; aplique-a apenas em etiquetas curtas.

## Componentes

### Botões e CTAs

- Forma: cantos soft edge, raio de `12px`; reservar `999px` para chips ou
  etiquetas, não para todos os botões.
- CTA primário: cor sólida `#52796F`, texto branco e peso 700. Use a cor
  secundária `#E7906D` somente para uma ação especialmente importante.
- Evite gradientes: a cor sólida favorece clareza e consistência no fluxo
  operacional.
- Hover: escurecer a cor, elevar `1px` e intensificar suavemente a sombra.
  Active retorna à posição original. Desabilitados não devem elevar nem sugerir
  interatividade.
- Preserve um foco de teclado visível em todos os botões e links.

### Cards e contêineres

- Superfície branca sobre fundo creme, borda de `1px solid #E7E1D8` e raio de
  `18px` (ou `16px` em telas pequenas).
- Sombra difusa e discreta: `0 12px 30px rgba(38, 53, 47, 0.08)`.
- Padding recomendado: `24px` em cards de formulário ou conteúdo; `16px` em
  cards compactos. Manter pelo menos `16px` entre grupos de controles.
- Campos usam raio `12px`; o foco destaca a borda sem mudar o tamanho do
  componente.

### Ícones e ilustrações

- Prefira vetores planos, formas simples e traços arredondados de espessura
  uniforme. Ícones minimalistas devem acompanhar texto quando a ação não for
  universalmente reconhecível.
- Ilustrações podem ter detalhes amistosos e poucos tons da paleta; evite
  excesso de elementos, caricaturas muito infantis e efeitos 3D realistas.
- Mantenha proporção e estilo consistentes entre as telas.

## Imagens e fotografia de pets

- Priorize fotografias autênticas de cães e gatos em contexto de cuidado,
  brincadeira ou descanso, com expressão tranquila e natural.
- Use luz natural difusa, balanço de branco neutro e fundos limpos, claros e
  pouco concorridos.
- Prefira enquadramentos próximos à altura dos olhos do animal; deixe respiro
  ao redor do rosto e não corte orelhas ou focinho de forma acidental.
- Mostre variedade de espécies, portes, idades e pelagens. Evite filtros
  saturados, flash duro, poses forçadas, acessórios excessivos e fundos que
  concorram com o animal.
- Aplique cantos arredondados às imagens para acompanhar os cards e preserve a
  proporção original para evitar distorções.

## Referência CSS

Os tokens abaixo correspondem à folha `assets/pettech.css`. Use-os em novos
elementos visuais para manter a identidade consistente.

```css
:root {
  --color-primary: #52796f;
  --color-primary-hover: #3e6259;
  --color-secondary: #e7906d;
  --color-secondary-hover: #cf7653;
  --color-background: #fbf8f3;
  --color-surface: #ffffff;
  --color-text: #26352f;
  --color-text-muted: #718078;
  --color-border: #e7e1d8;
  --color-focus: #e7906d;
  --shadow-card: 0 12px 30px rgba(38, 53, 47, 0.08);
}

body {
  background: var(--color-background);
  color: var(--color-text);
  font-family: "Nunito Sans", sans-serif;
}

.button-primary {
  background: var(--color-primary);
  border: 0;
  border-radius: 12px;
  color: var(--color-surface);
  font-weight: 700;
  transition: background-color 160ms ease, transform 160ms ease,
    box-shadow 160ms ease;
}

.button-primary:hover {
  background: var(--color-primary-hover);
  box-shadow: 0 7px 16px rgba(38, 53, 47, 0.14);
  transform: translateY(-1px);
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  box-shadow: var(--shadow-card);
  padding: 24px;
}
```

### Aplicação na interface atual

O tema é carregado globalmente em `Petech/Petech.py`; os tokens e estados de
hover/foco ficam em `assets/pettech.css`. As páginas, rotas, campos, estados e
ações existentes permanecem inalterados.
