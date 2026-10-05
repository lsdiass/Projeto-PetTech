// Delete SOLCANCELAMENTO record.
query "solcancelamento/{solcancelamento_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int solcancelamento_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.solcancelamento_id
    }
  }

  response = null
  guid = "eg0TjGEzIKXdlfY3qbF0moyj81g"
}