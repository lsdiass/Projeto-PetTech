// Autentica o Tutor sem revelar qual credencial está incorreta.
query "cliente/login" verb=POST {
  api_group = "Event Logs"
  description = "Autentica um cliente e retorna um token de acesso"

  input {
    email email filters=trim|lower
    text senha
  }

  stack {
    db.query tutor {
      where = $db.tutor.email == $input.email
      return = {type: "single"}
    } as $tutor

    precondition ($tutor != null && $tutor.password != null) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }

    security.check_password {
      text_password = $input.senha
      hash_password = $tutor.password
    } as $senha_valida

    precondition ($senha_valida) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }

    security.create_auth_token {
      table = "tutor"
      id = $tutor.id
      extras = {}
      expiration = 86400
    } as $auth_token
  }

  response = {
    authToken: $auth_token,
    tutor: {
      id: $tutor.id,
      nome: $tutor.nome,
      email: $tutor.email
    }
  }
  guid = "NlK_L4XY7-Kh3bVEnOJSKxPejM0"
}
