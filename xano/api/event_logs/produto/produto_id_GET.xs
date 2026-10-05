// Get PRODUTO record
query "produto/{produto_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int produto_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.produto_id
    } as $produto
  
    precondition ($produto != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $produto
  guid = "NJRX0S2X-_GF_GJ5mVKPvJFdzsQ"
}