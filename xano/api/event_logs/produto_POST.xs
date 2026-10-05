// Add PRODUTO record
query produto verb=POST {
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
    } as $produto
  }

  response = $produto
  guid = "MuXHFW-ZMyxf3Qz0ZCymB5wm4lw"
}