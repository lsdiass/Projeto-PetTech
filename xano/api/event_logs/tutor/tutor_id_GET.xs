// Get tutor record
query "tutor/{tutor_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int tutor_id? filters=min:1
  }

  stack {
    db.get tutor {
      field_name = "id"
      field_value = $input.tutor_id
    } as $tutor
  
    precondition ($tutor != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $tutor
  guid = "vI1MtspUJ1kgJ72AAJUxx4dUPSU"
}