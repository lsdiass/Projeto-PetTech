// Add TRANSAÇÃO record
query transa_o verb=POST {
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
    } as $transa_o
  }

  response = $transa_o
  guid = "zxb289qDLKkAJqiB6FgSLjMaD58"
}