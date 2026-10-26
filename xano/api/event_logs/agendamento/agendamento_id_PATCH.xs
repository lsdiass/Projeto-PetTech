// Update appointment status or service notes without changing the booked slot.
query "agendamento/{agendamento_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int agendamento_id? filters=min:1
    text? status? filters=trim
    text? observacoes_atendimento? filters=trim
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.get agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
    } as $agendamento_atual

    precondition ($agendamento_atual != null) {
      error_type = "notfound"
      error = "Agendamento não encontrado."
    }

    precondition ($input.status == null || $input.status == "Agendado" || $input.status == "Em Andamento" || $input.status == "Concluído" || $input.status == "Cancelado") {
      error_type = "inputerror"
      error = "O status informado não é válido."
    }

    precondition ($agendamento_atual.status != "Cancelado" || $input.status == null || $input.status == "Cancelado") {
      error_type = "inputerror"
      error = "Um agendamento cancelado não pode ser reativado."
    }

    var $campos_nao_permitidos {
      value = $raw_input|keys|diff:["status", "observacoes_atendimento"]
    }
    var $quantidade_campos_nao_permitidos {
      value = $campos_nao_permitidos|count
    }

    precondition ($quantidade_campos_nao_permitidos == 0) {
      error_type = "inputerror"
      error = "Somente status e observações podem ser atualizados."
    }

    var $dados_atualizacao {
      value = `$input|pick:($raw_input|keys)`|unpick:["agendamento_id"]|filter_null
    }
    var $quantidade_campos { value = $dados_atualizacao|keys|count }

    precondition ($quantidade_campos > 0) {
      error_type = "inputerror"
      error = "Informe um status ou uma observação para atualizar."
    }

    db.patch agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
      data = $dados_atualizacao
    } as $agendamento
  }

  response = $agendamento
  guid = "NqhYstDtBOF3gSofc1Fxl2rigkE"
}
