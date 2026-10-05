// Add CLIENTE record
query cliente verb=POST {
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
    } as $cliente
  }

  response = $cliente
  guid = "3CyDVQRjCgFCd8PG34qUjfMcZho"
}