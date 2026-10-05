// Delete OP record.
query "op/{op_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int op_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.op_id
    }
  }

  response = null
  guid = "TvvIToidAhoGPzlYAfNzhiMMA44"
}