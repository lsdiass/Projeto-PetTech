// Delete CLIENTE record.
query "cliente/{cliente_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.cliente_id
    }
  }

  response = null
  guid = "j3sVlKkgheyndy3_8Pmd6IBUFr0"
}