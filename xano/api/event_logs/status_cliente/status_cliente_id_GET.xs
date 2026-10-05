// Get STATUS_CLIENTE record
query "status_cliente/{status_cliente_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int status_cliente_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.status_cliente_id
    } as $status_cliente
  
    precondition ($status_cliente != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_cliente
  guid = "x55ySiK9TPqXTX-hlPV6vL0HqY8"
}