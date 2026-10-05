// Delete tokens record.
query "tokens/{tokens_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.tokens_id
    }
  }

  response = null
  guid = "f1iz9nBaRtHEm2TmnsMisLdg86Y"
}