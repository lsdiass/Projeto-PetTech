# Especificação: Navegação Administrativa

## Requisito: Navegação administrativa consistente

Todas as telas principais do painel administrativo MUST oferecer navegação
consistente para Tutores, Pets, Serviços, Novo Agendamento e Histórico. A seção
atual MUST ser identificada visualmente, e o acesso à área do cliente MUST
permanecer disponível. A navegação MUST continuar utilizável em telas estreitas.

### Cenário: Alternar entre seções

- **WHEN** o atendente está em uma tela administrativa
- **THEN** encontra os mesmos destinos de navegação em todas as telas principais
- **AND** a seção atual possui destaque visual

### Cenário: Acessar a área do cliente

- **WHEN** o atendente deseja abrir a área do cliente
- **THEN** pode acessá-la diretamente pela barra de navegação administrativa

### Cenário: Tela estreita

- **WHEN** o painel é aberto em viewport estreita
- **THEN** os links se reorganizam sem ficarem inacessíveis ou sobrepostos

### Cenário: Preservar operações

- **WHEN** o atendente usa formulários, listas ou ações administrativas
- **THEN** o comportamento existente continua disponível
