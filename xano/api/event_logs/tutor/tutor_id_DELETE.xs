// Delete tutor record.
query "tutor/{tutor_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int tutor_id? filters=min:1
  }

  stack {
    db.del tutor {
      field_name = "id"
      field_value = $input.tutor_id
    }
  }

  response = null
  guid = "zptg4uC6kHNsPHz1k_EaBmX58xI"
}