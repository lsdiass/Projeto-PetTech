// Query all OP records
query op verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $op
  }

  response = $op
  guid = "ypukGCCgEAF_dvg8QBS24MLZ2Ds"
}