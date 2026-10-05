// Query all STATUS_ITEM records
query status_item verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_item
  }

  response = $status_item
  guid = "v5H59dDRRs3ejasEc_VtNyfzLAM"
}