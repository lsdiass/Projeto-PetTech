table agendamento {
  auth = false

  schema {
    int id
    int pet_id
    int servico_id
    timestamp data_hora
    text status
    text? observacoes_atendimento?
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "pet_id"}]}
    {type: "btree", field: [{name: "servico_id"}]}
    {type: "btree", field: [{name: "data_hora"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "fYu9FOZ919Eosto5glPOoicCh4k"
}