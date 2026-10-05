// Query all ENDERECO records
query endereco verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $endereco
  }

  response = $endereco
  guid = "2xDZzugpoaIc51RAtymQkRdT3xo"
}