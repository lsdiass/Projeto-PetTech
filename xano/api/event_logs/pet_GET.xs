// Query all pet records
query pet verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query pet {
      return = {type: "list"}
    } as $pet
  }

  response = $pet
  guid = "usJsaDlNJArvldd1_S6JDklSyp0"
}