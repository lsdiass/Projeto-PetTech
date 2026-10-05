// Edit teste bobo record
query "teste_bobo/{teste_bobo_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int teste_bobo_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.teste_bobo_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $teste_bobo
  }

  response = $teste_bobo
  guid = "2i0ix_mYA6lhaX8p2KtuqrWTvvc"
}