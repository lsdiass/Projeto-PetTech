// Add pet record
query pet verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "pet"
    }
  }

  stack {
    db.add pet {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $pet
  }

  response = $pet
  guid = "aCU8-Unl0-igVrU6jTfkP_iAwb4"
}