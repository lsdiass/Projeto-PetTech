// Delete servico record.
query "servico/{servico_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int servico_id? filters=min:1
  }

  stack {
    db.del servico {
      field_name = "id"
      field_value = $input.servico_id
    }
  }

  response = null
  guid = "KeOXEr2Jloizs-N1tB_wqHR4420"
}