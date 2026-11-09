// Retorna somente os dados públicos do Tutor autenticado.
query "cliente/sessao/perfil" verb=GET {
  api_group = "Event Logs"
  auth = "tutor"
  description = "Retorna o perfil público do cliente autenticado"

  input {
  }

  stack {
    db.get tutor {
      field_name = "id"
      field_value = $auth.id
    } as $tutor

    precondition ($tutor != null) {
      error_type = "notfound"
      error = "Conta de cliente não encontrada."
    }
  }

  response = {
    id: $tutor.id,
    nome: $tutor.nome,
    email: $tutor.email
  }
  guid = "O5pr8ms-untVPtzdrn6bl95UKW0"
}
