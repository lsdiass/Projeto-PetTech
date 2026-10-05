// Get SOLCANCELAMENTO record
query "solcancelamento/{solcancelamento_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int solcancelamento_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.solcancelamento_id
    } as $solcancelamento
  
    precondition ($solcancelamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $solcancelamento
  guid = "NfBdapyEVtkj19uyTdS6yuBWi0g"
}