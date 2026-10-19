table tutor {
  auth = false

  schema {
    int id
    text nome
    text? email?
    text? telefone?
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "9TGscI-86-vpmFZ6N42Z-Xj-5yI"
}
