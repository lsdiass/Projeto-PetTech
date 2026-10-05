// Delete teste bobo record.
query "teste_bobo/{teste_bobo_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int teste_bobo_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.teste_bobo_id
    }
  }

  response = null
  guid = "ML2wjqRcDTLGU25i2WaNXaOU4K0"
}