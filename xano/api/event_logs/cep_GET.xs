// Query all CEP records
query cep verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cep
  }

  response = $cep
  guid = "gbGV0o17B9g4TQpEoJiQXCFT6Hg"
}