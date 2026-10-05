// Query all TTOKENIZACAO records
query ttokenizacao verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $ttokenizacao
  }

  response = $ttokenizacao
  guid = "vERn5Euypjpl2kKiNLvfvL68ZjE"
}