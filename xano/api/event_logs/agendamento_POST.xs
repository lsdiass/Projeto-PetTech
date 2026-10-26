// Creates an appointment after validating the Pet, Service, business hours and conflicts.
query agendamento verb=POST {
  api_group = "Event Logs"
  description = "Cria um agendamento com validação de disponibilidade"

  input {
    int pet_id filters=min:1
    int servico_id filters=min:1
    int data_hora filters=min:1
    text? observacoes_atendimento? filters=trim
  }

  stack {
    db.get pet {
      field_name = "id"
      field_value = $input.pet_id
    } as $pet

    precondition ($pet != null) {
      error_type = "inputerror"
      error = "O Pet selecionado não existe."
    }

    db.get servico {
      field_name = "id"
      field_value = $input.servico_id
    } as $servico

    precondition ($servico != null) {
      error_type = "inputerror"
      error = "O Serviço selecionado não existe."
    }

    precondition ($servico.duracao_minutos != null) {
      error_type = "inputerror"
      error = "O Serviço não possui uma duração cadastrada."
    }

    precondition ($servico.duracao_minutos|is_int) {
      error_type = "inputerror"
      error = "A duração do Serviço deve ser um número inteiro."
    }

    precondition ($servico.duracao_minutos > 0) {
      error_type = "inputerror"
      error = "O Serviço possui uma duração inválida."
    }

    var $inicio { value = $input.data_hora }
    var $fim { value = $inicio + ($servico.duracao_minutos * 60000) }
    var $data_local {
      value = $inicio|format_timestamp:"Y-m-d":"America/Sao_Paulo"
    }
    var $hora_local {
      value = $inicio|format_timestamp:"H:i":"America/Sao_Paulo"
    }
    var $hora_fim_local {
      value = $fim|format_timestamp:"H:i":"America/Sao_Paulo"
    }
    var $data_fim_local {
      value = $fim|format_timestamp:"Y-m-d":"America/Sao_Paulo"
    }
    var $minuto_local {
      value = $inicio|format_timestamp:"i":"America/Sao_Paulo"|to_int
    }
    var $segundo_local {
      value = $inicio|format_timestamp:"s":"America/Sao_Paulo"
    }
    var $resto_no_minuto { value = $inicio|modulus:60000 }
    var $ano { value = $inicio|format_timestamp:"Y":"America/Sao_Paulo"|to_int }
    var $ano_texto { value = $ano|to_text }

    var $a { value = $ano|modulus:19 }
    var $b { value = $ano|divide:100|floor }
    var $c { value = $ano - ($b * 100) }
    var $d { value = $b|divide:4|floor }
    var $e { value = $b|modulus:4 }
    var $f { value = ($b + 8)|divide:25|floor }
    var $g { value = ($b - $f + 1)|divide:3|floor }
    var $h { value = (19 * $a + $b - $d - $g + 15)|modulus:30 }
    var $i { value = $c|divide:4|floor }
    var $k { value = $c|modulus:4 }
    var $l { value = (32 + 2 * $e + 2 * $i - $h - $k)|modulus:7 }
    var $m { value = ($a + 11 * $h + 22 * $l)|divide:451|floor }
    var $mes_pascoa {
      value = ($h + $l - 7 * $m + 114)|divide:31|floor
    }
    var $dia_pascoa {
      value = (($h + $l - 7 * $m + 114)|modulus:31) + 1
    }
    var $data_pascoa {
      value = "%04d-%02d-%02d"|sprintf:$ano:$mes_pascoa:$dia_pascoa
    }
    var $sexta_santa {
      value = $data_pascoa|to_timestamp:"America/Sao_Paulo"
        |add_ms_to_timestamp:-172800000
        |format_timestamp:"Y-m-d":"America/Sao_Paulo"
    }
    var $feriados {
      value = [
        $ano_texto ~ "-01-01",
        $ano_texto ~ "-04-21",
        $ano_texto ~ "-05-01",
        $ano_texto ~ "-09-07",
        $ano_texto ~ "-10-12",
        $ano_texto ~ "-11-02",
        $ano_texto ~ "-11-15",
        $ano_texto ~ "-11-20",
        $ano_texto ~ "-12-25",
        $sexta_santa
      ]
    }
    var $feriado { value = false }

    foreach ($feriados) {
      each as $data_feriado {
        conditional {
          if ($data_feriado == $data_local) {
            var.update $feriado { value = true }
          }
        }
      }
    }

    precondition ($inicio > ("now"|to_timestamp:"America/Sao_Paulo")) {
      error_type = "inputerror"
      error = "Não é possível agendar em uma data ou horário passado."
    }

    precondition ($hora_local >= "08:00" && $hora_local < "18:00") {
      error_type = "inputerror"
      error = "O atendimento deve começar entre 08:00 e 17:30."
    }

    precondition ((($minuto_local|modulus:30) == 0) && $segundo_local == "00" && $resto_no_minuto == 0) {
      error_type = "inputerror"
      error = "O horário deve estar alinhado a intervalos de 30 minutos."
    }

    precondition ($data_fim_local == $data_local && $hora_fim_local <= "18:00") {
      error_type = "inputerror"
      error = "O serviço deve terminar até 18:00."
    }

    precondition (
      ($inicio|format_timestamp:"w":"America/Sao_Paulo") != "0"
    ) {
      error_type = "inputerror"
      error = "O estabelecimento não atende aos domingos."
    }

    precondition (!$feriado) {
      error_type = "inputerror"
      error = "O estabelecimento não atende em feriados nacionais."
    }

    var $dia_inicio {
      value = $data_local|to_timestamp:"America/Sao_Paulo"
    }
    var $dia_fim { value = $dia_inicio + 86400000 }

    db.transaction {
      stack {
        db.query agendamento {
          join = {
            servico: {
              table: "servico",
              type: "inner",
              where: $db.agendamento.servico_id == $db.servico.id
            }
          }
          eval = {
            duracao_minutos: $db.servico.duracao_minutos
          }
          where = $db.agendamento.data_hora >= $dia_inicio && $db.agendamento.data_hora < $dia_fim && $db.agendamento.status != "Cancelado"
          return = {type: "list"}
        } as $agendamentos

        var $conflito { value = false }

        foreach ($agendamentos) {
          each as $agendamento_existente {
            precondition ($agendamento_existente.duracao_minutos != null) {
              error_type = "inputerror"
              error = "Um Serviço vinculado a um agendamento existente não possui duração."
            }

            precondition ($agendamento_existente.duracao_minutos|is_int) {
              error_type = "inputerror"
              error = "Um Serviço vinculado a um agendamento existente possui duração inválida."
            }

            precondition ($agendamento_existente.duracao_minutos > 0) {
              error_type = "inputerror"
              error = "Um Serviço vinculado a um agendamento existente possui duração inválida."
            }

            var $inicio_existente {
              value = $agendamento_existente.data_hora
            }
            var $fim_existente {
              value = $inicio_existente + ($agendamento_existente.duracao_minutos * 60000)
            }

            conditional {
              if ($inicio < $fim_existente && $fim > $inicio_existente) {
                var.update $conflito { value = true }
              }
            }
          }
        }

        precondition (!$conflito) {
          error_type = "inputerror"
          error = "Este horário não está mais disponível."
        }

        db.add agendamento {
          data = {
            pet_id: $input.pet_id,
            servico_id: $input.servico_id,
            data_hora: $inicio,
            status: "Agendado",
            observacoes_atendimento: $input.observacoes_atendimento,
            created_at: "now"
          }
        } as $agendamento
      }
    }
  }

  response = $agendamento
  guid = "zcZz1ydUjD19qO8pc8ba4skGt8c"
}