// Get pet record
query "pet/{pet_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int pet_id? filters=min:1
  }

  stack {
    db.get pet {
      field_name = "id"
      field_value = $input.pet_id
    } as $pet
  
    precondition ($pet != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $pet
  guid = "ODjsiNJ5DOk618m5VnugkPVjpaQ"
}