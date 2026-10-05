// Add ITEM record
query item verb=POST {
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
    } as $item
  }

  response = $item
  guid = "xkjzhCdN9ZYsOB1MV_b5gm0MC8o"
}