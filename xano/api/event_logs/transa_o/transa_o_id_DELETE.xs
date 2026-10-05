// Delete TRANSAÇÃO record.
query "transa_o/{transa_o_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int transa_o_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.transa_o_id
    }
  }

  response = null
  guid = "6zKQ_6Dfn3OleVHeNdlG9XDwqZQ"
}