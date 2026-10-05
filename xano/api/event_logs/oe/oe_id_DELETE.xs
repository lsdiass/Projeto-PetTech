// Delete OE record.
query "oe/{oe_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.oe_id
    }
  }

  response = null
  guid = "OuXYGZB_VOFacKBXfGZKU4u_0xw"
}