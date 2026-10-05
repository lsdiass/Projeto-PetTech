// Get CLIENTE record
query "cliente/{cliente_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.cliente_id
    } as $cliente
  
    precondition ($cliente != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $cliente
  guid = "Y8s1wRgimGn5wK0fHx_indLnUzE"
}