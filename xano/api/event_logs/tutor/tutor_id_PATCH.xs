// Atualiza os dados de um tutor existente.
query "tutor/{tutor_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int tutor_id? filters=min:1
    text nome filters=trim
    email? email filters=trim|lower
    text? telefone filters=trim
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome é obrigatório."
    }

    db.get tutor {
      field_name = "id"
      field_value = $input.tutor_id
    } as $tutor_existente

    precondition ($tutor_existente != null) {
      error_type = "notfound"
      error = "Tutor não encontrado."
    }

    db.patch tutor {
      field_name = "id"
      field_value = $input.tutor_id
      data = {
        nome: $input.nome,
        email: $input.email,
        telefone: $input.telefone
      }
    } as $tutor_atualizado
  }

  response = $tutor_atualizado
  guid = "7kD6dxaT-h4gFiAvkO1zEaQC9wk"
}