// Query all CLIENTE records
query cliente verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "7L-s63okCy1eKCct_gGsVWZV3E0"
}