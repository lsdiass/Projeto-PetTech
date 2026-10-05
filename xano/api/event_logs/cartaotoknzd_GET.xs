// Query all CARTAOTOKNZD records
query cartaotoknzd verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
  guid = "A56fHj1HGtMRy-6YJwriL_HUwVk"
}