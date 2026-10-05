// Get teste bobo record
query "teste_bobo/{teste_bobo_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int teste_bobo_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.teste_bobo_id
    } as $teste_bobo
  
    precondition ($teste_bobo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $teste_bobo
  guid = "i0uZ38nH6448_H67ODdyMH30Cjc"
}