// Retorna o dashboard do Tutor autenticado com recursos vinculados à sua conta.
query "cliente/sessao/dashboard" verb=GET {
  api_group = "Event Logs"
  auth = "tutor"
  description = "Retorna perfil, Pets e Agendamentos do cliente autenticado"

  input {
  }

  stack {
    db.get tutor {
      field_name = "id"
      field_value = $auth.id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "notfound"
      error = "Conta de cliente não encontrada."
    }

    db.query pet {
      where = $db.pet.tutor_id == $auth.id
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $pets

    db.query agendamento {
      join = {
        pet: {
          table: "pet",
          type: "inner",
          where: $db.agendamento.pet_id == $db.pet.id
        },
        servico: {
          table: "servico",
          type: "inner",
          where: $db.agendamento.servico_id == $db.servico.id
        }
      }
      eval = {
        pet_nome: $db.pet.nome,
        servico_nome: $db.servico.nome
      }
      where = $db.pet.tutor_id == $auth.id
      sort = {data_hora: "desc"}
      return = {type: "list"}
    } as $agendamentos
  }

  response = {
    tutor: {
      id: $tutor.id,
      nome: $tutor.nome,
      cpf: $tutor.cpf,
      telefone: $tutor.telefone,
      email: $tutor.email
    },
    pets: $pets|map:{
      id: $$.id,
      nome: $$.nome,
      especie: $$.especie,
      raca: $$.raca,
      porte: $$.porte
    },
    agendamentos: $agendamentos|map:{
      id: $$.id,
      pet_nome: $$.pet_nome,
      servico_nome: $$.servico_nome,
      data_hora: $$.data_hora,
      status: $$.status
    }
  }
  guid = "yiszqR2M-0c-bY9Lbimvu4P4K1g"
}
