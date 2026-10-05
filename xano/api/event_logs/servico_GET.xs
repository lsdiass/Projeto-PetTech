// Query all servico records
query servico verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query servico {
      return = {type: "list"}
    } as $servico
  }

  response = $servico
  guid = "bhLRdhxVQjeZjbRVPgi_ajRzXo8"
}