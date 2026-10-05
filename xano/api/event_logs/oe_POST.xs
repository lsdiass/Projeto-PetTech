// Add OE record
query oe verb=POST {
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
    } as $oe
  }

  response = $oe
  guid = "SWB2Y6sI844uERcqOkUwOCzvR-M"
}