// Delete FAQ record.
query "faq/{faq_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.faq_id
    }
  }

  response = null
  guid = "iNxBTq82Jbxt09_j0Lm8Xlc3124"
}