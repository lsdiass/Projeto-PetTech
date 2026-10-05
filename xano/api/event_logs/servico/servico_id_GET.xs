// Get servico record
query "servico/{servico_id}" verb=GET {
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
      error = "Not Found."
    }
  }

  response = $servico
  guid = "O-ZqT9f031geooN5E1ZThiBzBPc"
}