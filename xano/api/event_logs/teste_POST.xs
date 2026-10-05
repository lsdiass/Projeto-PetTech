// Add teste record
query teste verb=POST {
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
    } as $teste
  }

  response = $teste
  guid = "g7hMdUquX1UU5CNNlsKgHgpzxtI"
}