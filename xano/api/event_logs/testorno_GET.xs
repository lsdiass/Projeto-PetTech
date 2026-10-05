// Query all TESTORNO records
query testorno verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $testorno
  }

  response = $testorno
  guid = "yHEpP18J3ttSporf85M6lsEtKH8"
}