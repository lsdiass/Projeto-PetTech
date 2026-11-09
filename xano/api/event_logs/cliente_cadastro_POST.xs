// Cria uma conta de Tutor com senha protegida por hash.
query "cliente/cadastro" verb=POST {
  api_group = "Event Logs"
  description = "Cria uma conta de cliente e retorna um token de autenticação"

  input {
    text nome filters=trim
    text cpf filters=trim
    text telefone filters=trim
    email email filters=trim|lower
    text senha
  }

  stack {
    var $cpf_normalizado {
      value = "/[^0-9]/"|regex_replace:"":$input.cpf
    }

    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome é obrigatório."
    }

    precondition ($input.telefone != "") {
      error_type = "inputerror"
      error = "O telefone é obrigatório."
    }

    precondition ("/^[0-9]{11}$/"|regex_matches:$cpf_normalizado) {
      error_type = "inputerror"
      error = "Informe um CPF com 11 dígitos."
    }

    precondition ("/^.{8,}$/"|regex_matches:$input.senha) {
      error_type = "inputerror"
      error = "A senha deve ter pelo menos 8 caracteres."
    }

    db.query tutor {
      where = $db.tutor.cpf == $cpf_normalizado
      return = {type: "single"}
    } as $tutor_com_cpf

    precondition ($tutor_com_cpf == null) {
      error_type = "inputerror"
      error = "Já existe uma conta com este CPF."
    }

    db.query tutor {
      where = $db.tutor.email == $input.email
      return = {type: "single"}
    } as $tutor_com_email

    precondition ($tutor_com_email == null) {
      error_type = "inputerror"
      error = "Já existe uma conta com este e-mail."
    }

    db.add tutor {
      data = {
        nome: $input.nome,
        cpf: $cpf_normalizado,
        telefone: $input.telefone,
        email: $input.email,
        password: $input.senha
      }
    } as $tutor

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
  guid = "H0QMAH4kLwqIaX5SGTthHY4ykNE"
}
