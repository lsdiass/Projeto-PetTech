// Delete ITEM record.
query "item/{item_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int item_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.item_id
    }
  }

  response = null
  guid = "PYSiZRV7tDDU_KorjErpDAdUwOE"
}