// Edit CARTAOTOKNZD record
query "cartaotoknzd/{cartaotoknzd_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int cartaotoknzd_id? filters=min:1
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
      field_value = $input.cartaotoknzd_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
  guid = "2pr95R0tKUVXDvgyBMmmOmg-tm8"
}