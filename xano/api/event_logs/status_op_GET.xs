// Query all STATUS_OP records
query status_op verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_op
  }

  response = $status_op
  guid = "bpwF3t0tq5Y0ncH03uAcUpF_M_E"
}