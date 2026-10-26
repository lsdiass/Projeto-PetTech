// Edit servico record
query "servico/{servico_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int servico_id? filters=min:1
    text nome filters=trim
    text? descricao filters=trim
    decimal preco
    int duracao_minutos filters=min:1
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do serviço é obrigatório."
    }

    precondition ($input.preco > 0) {
      error_type = "inputerror"
      error = "O preço deve ser maior que zero."
    }

    db.get servico {
      field_name = "id"
      field_value = $input.servico_id
    } as $servico_existente

    precondition ($servico_existente != null) {
      error_type = "notfound"
      error = "Serviço não encontrado."
    }
  
    db.patch servico {
      field_name = "id"
      field_value = $input.servico_id
      data = {
        nome: $input.nome,
        descricao: $input.descricao,
        preco: $input.preco,
        duracao_minutos: $input.duracao_minutos
      }
    } as $servico
  }

  response = $servico
  guid = "8SN7gOWvKP7OMGftSFFvtp9ooys"
}