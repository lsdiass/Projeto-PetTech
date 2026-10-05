// Delete STATUS_OE record.
query "status_oe/{status_oe_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int status_oe_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_oe_id
    }
  }

  response = null
  guid = "wuoa6KgECP5j2HJLpn2c2WlFitk"
}