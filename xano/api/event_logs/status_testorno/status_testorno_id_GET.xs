// Get STATUS_TESTORNO record
query "status_testorno/{status_testorno_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int status_testorno_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.status_testorno_id
    } as $status_testorno
  
    precondition ($status_testorno != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_testorno
  guid = "b7ByGcCfx31v3QjErXXrB4Ao8h8"
}