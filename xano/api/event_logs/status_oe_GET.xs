// Query all STATUS_OE records
query status_oe verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_oe
  }

  response = $status_oe
  guid = "3HLItvZVHy694myXv5UzjYQ-O3w"
}