// Get OE record
query "oe/{oe_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.oe_id
    } as $oe
  
    precondition ($oe != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $oe
  guid = "QFwHD4eNQKxaOa3cuiJtjGC4M34"
}