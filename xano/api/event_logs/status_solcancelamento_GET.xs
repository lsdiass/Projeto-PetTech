// Query all STATUS_SOLCANCELAMENTO records
query status_solcancelamento verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_solcancelamento
  }

  response = $status_solcancelamento
  guid = "QjzKhKDuftfk9EhEdD7xGUzfBVI"
}