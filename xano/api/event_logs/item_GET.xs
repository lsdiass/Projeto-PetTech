// Query all ITEM records
query item verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $item
  }

  response = $item
  guid = "Fao4wsDaZMr_kL8oR0dY1T76haI"
}