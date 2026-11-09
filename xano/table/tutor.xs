table tutor {
  auth = true

  schema {
    int id
    text nome
    text? cpf? {
      sensitive = true
    }
    email? email? filters=trim|lower {
      sensitive = true
    }
    text? telefone?
    password? password? {
      sensitive = true
    }
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cpf"}]}
    {type: "btree|unique", field: [{name: "email"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "9TGscI-86-vpmFZ6N42Z-Xj-5yI"
}
