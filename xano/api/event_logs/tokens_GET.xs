// Query all tokens records
query tokens verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $tokens
  }

  response = $tokens
  guid = "AA3jrHQXzjTYUfs2vO26Mr5UUpM"
}