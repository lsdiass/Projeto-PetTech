// Add PAPEL record
query papel verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $papel
  }

  response = $papel
  guid = "edswWePWC7ThrLaUHr3xyRIxBSs"
}