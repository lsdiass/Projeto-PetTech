table servico {
  auth = false

  schema {
    int id
    text nome
    text? descricao?
    decimal preco
    int duracao_minutos
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "qhyGlk-v0jsFqtu6ILcLnokySro"
}