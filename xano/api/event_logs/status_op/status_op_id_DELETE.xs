// Delete STATUS_OP record.
query "status_op/{status_op_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_op_id
    }
  }

  response = null
  guid = "zKysKlvrII9u-DS0nKgBKTFq0fQ"
}