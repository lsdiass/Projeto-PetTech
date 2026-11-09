# Dashboard da Área do Cliente

## Por que

Após entrar na área do cliente, o Tutor precisa consultar seus dados cadastrais,
os Pets sob sua responsabilidade e os Agendamentos relacionados sem acessar
informações de outros Tutores.

## O que muda

- Substitui a página inicial mínima do cliente por um dashboard.
- Exibe nome, CPF, telefone e e-mail do Tutor autenticado.
- Lista os Pets vinculados ao Tutor.
- Separa Agendamentos ativos do histórico, mostrando Pet, Serviço, data, hora e
  status.
- Carrega os dados por endpoint autenticado no Xano, que aplica o vínculo do
  Tutor no backend.
- Mantém a ação de sair e os fluxos administrativos existentes.

## Capacidades

### Novas capacidades

- `dashboard-cliente`: consulta agregada de perfil, Pets e Agendamentos do
  Tutor autenticado.

### Capacidades modificadas

- `conta-cliente-tutor`: apresenta um dashboard na página inicial após o login.

## Impacto

- Xano: novo endpoint autenticado de dashboard, com leitura de Tutor, Pet,
  Servico e Agendamento existentes.
- Frontend Reflex: estado, carregamento e visualização em
  `Petech/Petech.py`.
- Documentação do escopo de clientes.
- Não cria entidades, altera registros operacionais nem adiciona ações de
  alteração/cancelamento.
