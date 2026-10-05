// Delete PAPEL record.
query "papel/{papel_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int papel_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.papel_id
    }
  }

  response = null
  guid = "6Wkj-98Qu6ELRY8_tAwRwSV16_Y"
}