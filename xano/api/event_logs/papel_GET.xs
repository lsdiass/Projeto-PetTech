// Query all PAPEL records
query papel verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
  guid = "VxGz1s_sQ9oAS1mbs5EObqPJBLM"
}