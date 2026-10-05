// Delete STATUS_SOLCANCELAMENTO record.
query "status_solcancelamento/{status_solcancelamento_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int status_solcancelamento_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_solcancelamento_id
    }
  }

  response = null
  guid = "Resx1fEygoE0eO1rtI1PrwP5x2U"
}