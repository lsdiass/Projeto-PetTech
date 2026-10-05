// Add servico record
query servico verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "servico"
    }
  }

  stack {
    db.add servico {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $servico
  }

  response = $servico
  guid = "sJyyn1ks_dTP8dF7jSH6N27kNWY"
}