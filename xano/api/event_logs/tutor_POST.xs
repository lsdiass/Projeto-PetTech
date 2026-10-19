// Add tutor record
query "tutor" verb=POST {
  api_group = "Event Logs"
  description = "Cadastra um novo tutor"

  input {
    text nome filters=trim
    email email? filters=trim|lower
    text telefone? filters=trim
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome é obrigatório."
    }

    db.add tutor {
      enforce_hidden_fields = false
      data = {
        nome: $input.nome,
        email: $input.email,
        telefone: $input.telefone,
        created_at: "now"
      }
    } as $tutor
  }

  response = $tutor
  guid = "3BxQ3_3fRohV0xn8ppFuQYluzGE"
}
