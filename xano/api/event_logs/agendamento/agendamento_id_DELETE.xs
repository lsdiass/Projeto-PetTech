// Delete agendamento record.
query "agendamento/{agendamento_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int agendamento_id? filters=min:1
  }

  stack {
    db.del agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
    }
  }

  response = null
  guid = "IYDW3cwQnIHQwYJwg--1PiBPG0w"
}