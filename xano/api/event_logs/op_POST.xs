// Add OP record
query op verb=POST {
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
    } as $op
  }

  response = $op
  guid = "hmjXk-tAi_BJ8TsbK6dv4_lPPdU"
}