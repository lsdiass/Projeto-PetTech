// Get ITEM record
query "item/{item_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int item_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.item_id
    } as $item
  
    precondition ($item != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $item
  guid = "f9np-NiUunKOX5anC78JodMyJr0"
}