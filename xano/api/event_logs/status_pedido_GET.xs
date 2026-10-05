// Query all STATUS_PEDIDO records
query status_pedido verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_pedido
  }

  response = $status_pedido
  guid = "6jPPMuXD4eQC4C2xaxZF0eMby4E"
}