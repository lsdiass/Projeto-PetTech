// Add STATUS_OP record
query status_op verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_op
  }

  response = $status_op
  guid = "fNHKj2rBYOVFFrovMZTOpdkxMLo"
}