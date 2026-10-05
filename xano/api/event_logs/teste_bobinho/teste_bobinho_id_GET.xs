// Get teste_bobinho record
query "teste_bobinho/{teste_bobinho_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int teste_bobinho_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.teste_bobinho_id
    } as $teste_bobinho
  
    precondition ($teste_bobinho != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $teste_bobinho
  guid = "Sxrd5gPPb1NQwGzrAffxidLLuw0"
}