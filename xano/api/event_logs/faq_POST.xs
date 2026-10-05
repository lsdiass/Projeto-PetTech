// Add FAQ record
query faq verb=POST {
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
    } as $faq
  }

  response = $faq
  guid = "6zJ4nC2OnqE7tKnuBlW-HBQ2xkQ"
}