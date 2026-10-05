// Edit agendamento record
query "agendamento/{agendamento_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int agendamento_id? filters=min:1
    dblink {
      table = "agendamento"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $agendamento
  }

  response = $agendamento
  guid = "NqhYstDtBOF3gSofc1Fxl2rigkE"
}