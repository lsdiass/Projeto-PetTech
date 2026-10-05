// Get TTOKENIZACAO record
query "ttokenizacao/{ttokenizacao_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int ttokenizacao_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.ttokenizacao_id
    } as $ttokenizacao
  
    precondition ($ttokenizacao != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $ttokenizacao
  guid = "KAt73kFFjagxVo8UwSviKdIhVfA"
}