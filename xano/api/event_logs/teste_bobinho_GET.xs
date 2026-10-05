// Query all teste_bobinho records
query teste_bobinho verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $teste_bobinho
  }

  response = $teste_bobinho
  guid = "Tw2wwH67UlAvxe3WWLhWctMTA9g"
}