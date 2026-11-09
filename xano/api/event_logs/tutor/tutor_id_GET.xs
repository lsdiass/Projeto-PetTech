// Get tutor record
query "tutor/{tutor_id}" verb=GET {
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
      error = "Not Found."
    }
  }

  response = {
    id: $tutor.id,
    nome: $tutor.nome,
    email: $tutor.email,
    telefone: $tutor.telefone
  }
  guid = "vI1MtspUJ1kgJ72AAJUxx4dUPSU"
}