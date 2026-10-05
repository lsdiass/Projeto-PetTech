// Delete ENDERECO record.
query "endereco/{endereco_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int endereco_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.endereco_id
    }
  }

  response = null
  guid = "Wwx3B3AsOtAydA4u-gTWKGXRxdQ"
}