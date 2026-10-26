// Add servico record
query servico verb=POST {
  api_group = "Event Logs"
  description = "Cadastra um serviço do catálogo"

  input {
    text nome filters=trim
    text? descricao? filters=trim
    decimal preco
    decimal duracao_minutos filters=min:1
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

    precondition (
      $input.duracao_minutos > 0 &&
      $input.duracao_minutos == ($input.duracao_minutos|to_int)
    ) {
      error_type = "inputerror"
      error = "A duração deve ser um número inteiro maior que zero."
    }

    db.add servico {
      enforce_hidden_fields = false
      data = {
        nome: $input.nome,
        descricao: $input.descricao,
        preco: $input.preco,
        duracao_minutos: $input.duracao_minutos|to_int,
        created_at: "now"
      }
    } as $servico
  }

  response = $servico
  guid = "sJyyn1ks_dTP8dF7jSH6N27kNWY"
}