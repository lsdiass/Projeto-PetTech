// Add STATUS_SOLCANCELAMENTO record
query status_solcancelamento verb=POST {
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
    } as $status_solcancelamento
  }

  response = $status_solcancelamento
  guid = "_u2WgJ8UT0mYiXQISm7a0m_0at0"
}