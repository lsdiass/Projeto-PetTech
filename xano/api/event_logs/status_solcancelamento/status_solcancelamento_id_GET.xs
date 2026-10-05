// Get STATUS_SOLCANCELAMENTO record
query "status_solcancelamento/{status_solcancelamento_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int status_solcancelamento_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.status_solcancelamento_id
    } as $status_solcancelamento
  
    precondition ($status_solcancelamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_solcancelamento
  guid = "U39ErD8-J6ow52Lxl-yyICHt_NA"
}