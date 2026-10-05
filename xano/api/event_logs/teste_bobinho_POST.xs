// Add teste_bobinho record
query teste_bobinho verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $teste_bobinho
  }

  response = $teste_bobinho
  guid = "BLGeblgZ0r_KTfOKoXiARnskofk"
}