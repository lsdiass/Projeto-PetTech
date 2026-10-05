// Add TTOKENIZACAO record
query ttokenizacao verb=POST {
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
    } as $ttokenizacao
  }

  response = $ttokenizacao
  guid = "lMQ5Lrei9o5eTcMzWFXbDTwtIw4"
}