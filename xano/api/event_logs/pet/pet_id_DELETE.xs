// Exclui um pet somente quando não há agendamentos vinculados.
query "pet/{pet_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int pet_id? filters=min:1
  }

  stack {
    db.get pet {
      field_name = "id"
      field_value = $input.pet_id
    } as $pet

    precondition ($pet != null) {
      error_type = "notfound"
      error = "Pet não encontrado."
    }

    db.query agendamento {
      where = $db.agendamento.pet_id == $input.pet_id
      return = {type: "count"}
    } as $agendamentos_vinculados

    precondition ($agendamentos_vinculados == 0) {
      error_type = "inputerror"
      error = "Não é possível excluir um pet que possui agendamentos."
    }

    db.del pet {
      field_name = "id"
      field_value = $input.pet_id
    }
  }

  response = {
    id: $input.pet_id,
    deleted: true
  }
  guid = "wWHx0ZJYTr6lQZHtksRU2RFjnu8"
}