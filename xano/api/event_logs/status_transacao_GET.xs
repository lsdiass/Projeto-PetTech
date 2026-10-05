// Query all STATUS_TRANSACAO records
query status_transacao verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_transacao
  }

  response = $status_transacao
  guid = "mELGRgKBsa_I-dzx9yOgP4BvecE"
}