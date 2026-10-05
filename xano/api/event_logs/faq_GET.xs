// Query all FAQ records
query faq verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $faq
  }

  response = $faq
  guid = "KXY_dQyeEgmO97HGCUrDwLuWpj8"
}