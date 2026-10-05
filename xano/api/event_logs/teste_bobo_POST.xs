// Add teste bobo record
query teste_bobo verb=POST {
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
    } as $teste_bobo
  }

  response = $teste_bobo
  guid = "-lgrSE3nc8ZCKTSqna6379Oz4Vs"
}