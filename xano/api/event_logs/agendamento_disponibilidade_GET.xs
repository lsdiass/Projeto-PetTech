// Returns the available start times for every day of a requested month.
query agendamento_disponibilidade verb=GET {
  api_group = "Event Logs"
  description = "Consulta horários de agendamento disponíveis por serviço e mês"

  input {
    int servico_id filters=min:1
    int ano filters=min:2020
    int mes filters=min:1
  }

  stack {
    precondition ($input.mes <= 12) {
      error_type = "inputerror"
      error = "O mês deve estar entre 1 e 12."
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

    var $mes_texto { value = "%04d-%02d"|sprintf:$input.ano:$input.mes }
    var $inicio_mes {
      value = ($mes_texto ~ "-01")|to_timestamp:"America/Sao_Paulo"
    }
    var $fim_consulta { value = $inicio_mes + 2764800000 }
    var $mes_atual {
      value = "now"|format_timestamp:"Y-m":"America/Sao_Paulo"
    }

    precondition ($mes_texto >= $mes_atual) {
      error_type = "inputerror"
      error = "Não é possível consultar meses passados."
    }

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
      where = $db.agendamento.data_hora >= $inicio_mes && $db.agendamento.data_hora < $fim_consulta && $db.agendamento.status != "Cancelado"
      return = {type: "list"}
    } as $agendamentos

    var $dias { value = [] }
    var $ano_texto { value = $input.ano|to_text }

    var $a { value = $input.ano|modulus:19 }
    var $b { value = $input.ano|divide:100|floor }
    var $c { value = $input.ano - ($b * 100) }
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
      value = "%04d-%02d-%02d"|sprintf:$input.ano:$mes_pascoa:$dia_pascoa
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

    foreach (0..30) {
      each as $deslocamento_dia {
        var $dia_timestamp {
          value = $inicio_mes + ($deslocamento_dia * 86400000)
        }
        var $data_local {
          value = $dia_timestamp|format_timestamp:"Y-m-d":"America/Sao_Paulo"
        }
        var $mes_dia {
          value = $dia_timestamp|format_timestamp:"Y-m":"America/Sao_Paulo"
        }
        var $horarios { value = [] }
        var $tem_horario_disponivel { value = false }
        var $agendamentos_do_dia { value = [] }

        foreach ($agendamentos) {
          each as $agendamento_existente {
            var $data_agendamento {
              value = $agendamento_existente.data_hora
                |format_timestamp:"Y-m-d":"America/Sao_Paulo"
            }
            conditional {
              if ($data_agendamento == $data_local) {
                var.update $agendamentos_do_dia {
                  value = $agendamentos_do_dia|push:$agendamento_existente
                }
              }
            }
          }
        }

        conditional {
          if ($mes_dia == $mes_texto) {
            var $dia_semana {
              value = $dia_timestamp|format_timestamp:"w":"America/Sao_Paulo"
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

            conditional {
              if ($dia_semana != "0" && !$feriado) {
                foreach (0..19) {
                  each as $indice_horario {
                    var $inicio_horario {
                      value = $dia_timestamp + ((480 + ($indice_horario * 30)) * 60000)
                    }
                    var $fim_horario {
                      value = $inicio_horario + ($servico.duracao_minutos * 60000)
                    }
                    var $data_fim_horario {
                      value = $fim_horario|format_timestamp:"Y-m-d":"America/Sao_Paulo"
                    }
                    var $fim_horario_texto {
                      value = $fim_horario
                        |format_timestamp:"H:i":"America/Sao_Paulo"
                    }

                    conditional {
                      if ($inicio_horario >= ("now"|to_timestamp:"America/Sao_Paulo") && $data_fim_horario == $data_local && $fim_horario_texto <= "18:00") {
                        var $disponivel { value = true }

                        foreach ($agendamentos_do_dia) {
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
                              if ($inicio_horario < $fim_existente && $fim_horario > $inicio_existente) {
                                var.update $disponivel { value = false }
                              }
                            }
                          }
                        }

                        var $hora_texto {
                          value = $inicio_horario
                            |format_timestamp:"H:i":"America/Sao_Paulo"
                        }
                        var $horario {
                          value = {
                            data_hora: $inicio_horario,
                            hora: $hora_texto,
                            disponivel: $disponivel
                          }
                        }
                        var.update $horarios {
                          value = $horarios|push:$horario
                        }

                        conditional {
                          if ($disponivel) {
                            var.update $tem_horario_disponivel { value = true }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }

        conditional {
          if ($mes_dia == $mes_texto) {
            var $dia {
              value = {
                data: $data_local,
                horarios: $horarios,
                tem_horario_disponivel: $tem_horario_disponivel
              }
            }
            var.update $dias { value = $dias|push:$dia }
          }
        }
      }
    }
  }

  response = $dias
  guid = "dsq1evZnF3lf1fiLIvZoP2wGqyU"
}
