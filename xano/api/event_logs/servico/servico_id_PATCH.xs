// Edit servico record
query "servico/{servico_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int servico_id? filters=min:1
    dblink {
      table = "servico"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch servico {
      field_name = "id"
      field_value = $input.servico_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $servico
  }

  response = $servico
  guid = "8SN7gOWvKP7OMGftSFFvtp9ooys"
}