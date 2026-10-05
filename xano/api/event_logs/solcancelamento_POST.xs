// Add SOLCANCELAMENTO record
query solcancelamento verb=POST {
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
    } as $solcancelamento
  }

  response = $solcancelamento
  guid = "HVdxeb2ACugEbBeLgCyp-JnNJDo"
}