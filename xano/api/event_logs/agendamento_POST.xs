// Add agendamento record
query agendamento verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "agendamento"
    }
  }

  stack {
    db.add agendamento {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $agendamento
  }

  response = $agendamento
  guid = "zcZz1ydUjD19qO8pc8ba4skGt8c"
}