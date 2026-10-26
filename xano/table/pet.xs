table pet {
  auth = false

  schema {
    int id
    int tutor_id
    text nome
    text especie
    text? raca?
    text porte
    text? observacoes_saude?
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "tutor_id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "IareXzIgCcwrkezQefo_L9fSqUU"
}