// Query all tutor records
query tutor verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query tutor {
      return = {type: "list"}
    } as $tutor
  }

  response = $tutor|map:{id: $$.id, nome: $$.nome, email: $$.email, telefone: $$.telefone}
  guid = "FLbnSVNj9OGNX5J-B5aO45-j1mU"
}