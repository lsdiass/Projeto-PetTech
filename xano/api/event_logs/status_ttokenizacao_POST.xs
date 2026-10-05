// Add STATUS_TTOKENIZACAO record
query status_ttokenizacao verb=POST {
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
    } as $status_ttokenizacao
  }

  response = $status_ttokenizacao
  guid = "2wo4LuqG8pMgIzblKsWmLm5HJpU"
}