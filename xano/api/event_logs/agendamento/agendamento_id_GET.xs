// Get agendamento record
query "agendamento/{agendamento_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int agendamento_id? filters=min:1
  }

  stack {
    db.get agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
    } as $agendamento
  
    precondition ($agendamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $agendamento
  guid = "6dfhPt-3SeQm2yn_KmcpNW9HglA"
}