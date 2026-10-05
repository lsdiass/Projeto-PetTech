// Query all OE records
query oe verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $oe
  }

  response = $oe
  guid = "X2zDLZMZhl-F5Yk-q9nuulYhsdQ"
}