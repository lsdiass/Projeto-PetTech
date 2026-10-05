// Delete teste_bobinho record.
query "teste_bobinho/{teste_bobinho_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int teste_bobinho_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.teste_bobinho_id
    }
  }

  response = null
  guid = "LxaQDzwUfeHtDWhz5lIXI7nxKlE"
}