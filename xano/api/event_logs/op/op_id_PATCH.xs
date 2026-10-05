// Edit OP record
query "op/{op_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int op_id? filters=min:1
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
      field_value = $input.op_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $op
  }

  response = $op
  guid = "cIWW7WPdqLWNEGHgcvXZgqM8Yzk"
}