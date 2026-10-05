// Add tutor record
query tutor verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "tutor"
    }
  }

  stack {
    db.add tutor {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $tutor
  }

  response = $tutor
  guid = "3BxQ3_3fRohV0xn8ppFuQYluzGE"
}