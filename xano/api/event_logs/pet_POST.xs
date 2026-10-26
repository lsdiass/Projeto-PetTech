// Add pet record
query pet verb=POST {
  api_group = "Event Logs"
  description = "Cadastra um pet vinculado a um tutor existente"

  input {
    int tutor_id filters=min:1
    text nome filters=trim
    text especie filters=trim
    text? raca? filters=trim
    text porte filters=trim
    text? observacoes_saude? filters=trim
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do pet é obrigatório."
    }

    precondition ($input.especie != "") {
      error_type = "inputerror"
      error = "A espécie do pet é obrigatória."
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
      field_value = $input.tutor_id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "inputerror"
      error = "O tutor informado não existe."
    }

    db.add pet {
      enforce_hidden_fields = false
      data = {
        tutor_id: $input.tutor_id,
        nome: $input.nome,
        especie: $input.especie,
        raca: $input.raca,
        porte: $input.porte,
        observacoes_saude: $input.observacoes_saude,
        created_at: "now"
      }
    } as $pet
  }

  response = $pet
  guid = "aCU8-Unl0-igVrU6jTfkP_iAwb4"
}