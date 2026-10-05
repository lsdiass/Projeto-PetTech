// Add TESTORNO record
query testorno verb=POST {
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
    } as $testorno
  }

  response = $testorno
  guid = "E76p3vVgKRg5gicP8enboCcv1Ig"
}