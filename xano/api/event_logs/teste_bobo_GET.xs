// Query all teste bobo records
query teste_bobo verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $teste_bobo
  }

  response = $teste_bobo
  guid = "Nrb3xM2lzbZbLS_ijjC16ZMLqEw"
}