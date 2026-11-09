// Cadastra um Pet exclusivamente para o Tutor autenticado.
query "cliente/sessao/pets" verb=POST {
  api_group = "Event Logs"
  auth = "tutor"
  description = "Cadastra um Pet para o Tutor autenticado"

  input {
    text nome filters=trim
    text especie filters=trim
    text? raca? filters=trim
    text porte filters=trim
    text? observacoes_saude? filters=trim
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do Pet é obrigatório."
    }

    precondition ($input.especie != "") {
      error_type = "inputerror"
      error = "A espécie do Pet é obrigatória."
    }

    precondition (
      $input.porte == "Pequeno" ||
      $input.porte == "Médio" ||
      $input.porte == "Grande"
    ) {
      error_type = "inputerror"
      error = "O porte deve ser Pequeno, Médio ou Grande."
    }

    db.get tutor {
      field_name = "id"
      field_value = $auth.id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "notfound"
      error = "Conta de cliente não encontrada."
    }

    db.add pet {
      data = {
        tutor_id: $auth.id,
        nome: $input.nome,
        especie: $input.especie,
        raca: $input.raca,
        porte: $input.porte,
        observacoes_saude: $input.observacoes_saude,
        created_at: "now"
      }
    } as $pet
  }

  response = {
    id: $pet.id,
    tutor_id: $pet.tutor_id,
    nome: $pet.nome,
    especie: $pet.especie,
    raca: $pet.raca,
    porte: $pet.porte,
    observacoes_saude: $pet.observacoes_saude
  }
  guid = "fxnTXu54vpw1cbuEeQZo0l7xkyw"
}
