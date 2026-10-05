// Add CARTAOTOKNZD record
query cartaotoknzd verb=POST {
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
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
  guid = "1oIVG8yXhQBOBKxz0mQXiMEiaNU"
}