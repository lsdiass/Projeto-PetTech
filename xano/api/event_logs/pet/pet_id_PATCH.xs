// Edit pet record
query "pet/{pet_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int pet_id? filters=min:1
    dblink {
      table = "pet"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch pet {
      field_name = "id"
      field_value = $input.pet_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $pet
  }

  response = $pet
  guid = "qFxsgH94hxsLLhiE4YX488Tnz3U"
}