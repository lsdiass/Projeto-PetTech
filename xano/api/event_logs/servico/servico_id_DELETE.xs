// Exclui um serviço somente quando não há agendamentos vinculados.
query "servico/{servico_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int servico_id? filters=min:1
  }

  stack {
    db.get servico {
      field_name = "id"
      field_value = $input.servico_id
    } as $servico

    precondition ($servico != null) {
      error_type = "notfound"
      error = "Serviço não encontrado."
    }

    db.query agendamento {
      where = $db.agendamento.servico_id == $input.servico_id
      return = {type: "count"}
    } as $agendamentos_vinculados

    precondition ($agendamentos_vinculados == 0) {
      error_type = "inputerror"
      error = "Não é possível excluir um serviço que possui agendamentos."
    }

    db.del servico {
      field_name = "id"
      field_value = $input.servico_id
    }
  }

  response = {
    id: $input.servico_id,
    deleted: true
  }
  guid = "KeOXEr2Jloizs-N1tB_wqHR4420"
}