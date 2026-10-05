// Add STATUS_CLIENTE record
query status_cliente verb=POST {
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
    } as $status_cliente
  }

  response = $status_cliente
  guid = "_wAKZ9EdtcM30knYxlEn-dh2NmU"
}