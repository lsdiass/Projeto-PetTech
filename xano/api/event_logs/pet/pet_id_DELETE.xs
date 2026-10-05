// Delete pet record.
query "pet/{pet_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int pet_id? filters=min:1
  }

  stack {
    db.del pet {
      field_name = "id"
      field_value = $input.pet_id
    }
  }

  response = null
  guid = "wWHx0ZJYTr6lQZHtksRU2RFjnu8"
}