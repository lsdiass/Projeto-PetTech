// Add STATUS_OE record
query status_oe verb=POST {
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
    } as $status_oe
  }

  response = $status_oe
  guid = "lBfQaSLkX44rhI8bVXmWfYnxJHw"
}