// Edit pet record
query "pet/{pet_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int pet_id? filters=min:1
    int tutor_id filters=min:1
    text nome filters=trim
    text especie filters=trim
    text? raca filters=trim
    text porte filters=trim
    text? observacoes_saude filters=trim
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

    db.get pet {
      field_name = "id"
      field_value = $input.pet_id
    } as $pet_existente

    precondition ($pet_existente != null) {
      error_type = "notfound"
      error = "Pet não encontrado."
    }

    db.get tutor {
      field_name = "id"
      field_value = $input.tutor_id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "inputerror"
      error = "O tutor informado não existe."
    }
  
    db.patch pet {
      field_name = "id"
      field_value = $input.pet_id
      data = {
        tutor_id: $input.tutor_id,
        nome: $input.nome,
        especie: $input.especie,
        raca: $input.raca,
        porte: $input.porte,
        observacoes_saude: $input.observacoes_saude
      }
    } as $pet
  }

  response = $pet
  guid = "qFxsgH94hxsLLhiE4YX488Tnz3U"
}