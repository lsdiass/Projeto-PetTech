// Query all agendamento records
query agendamento verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query agendamento {
      return = {type: "list"}
    } as $agendamento
  }

  response = $agendamento
  guid = "1FNXNMe9Tt4Af8xg-CfpYndkB0U"
}