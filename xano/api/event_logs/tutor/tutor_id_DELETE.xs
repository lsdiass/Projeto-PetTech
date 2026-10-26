// Exclui um tutor somente quando não há pets vinculados.
query "tutor/{tutor_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int tutor_id? filters=min:1
  }

  stack {
    db.get tutor {
      field_name = "id"
      field_value = $input.tutor_id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "notfound"
      error = "Tutor não encontrado."
    }

    db.query pet {
      where = $db.pet.tutor_id == $input.tutor_id
      return = {type: "count"}
    } as $pets_vinculados

    precondition ($pets_vinculados == 0) {
      error_type = "inputerror"
      error = "Não é possível excluir um tutor que possui pets vinculados."
    }

    db.del tutor {
      field_name = "id"
      field_value = $input.tutor_id
    }
  }

  response = {
    id: $input.tutor_id,
    deleted: true
  }
  guid = "zptg4uC6kHNsPHz1k_EaBmX58xI"
}