// Get STATUS_PEDIDO record
query "status_pedido/{status_pedido_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int status_pedido_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.status_pedido_id
    } as $status_pedido
  
    precondition ($status_pedido != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_pedido
  guid = "O2z0h8X-gFcdPq26EMAW9c6oXaY"
}