// Query all PRODUTO records
query produto verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $produto
  }

  response = $produto
  guid = "zTaL0vY4zTJ-3bXmo3adc9tvEFY"
}