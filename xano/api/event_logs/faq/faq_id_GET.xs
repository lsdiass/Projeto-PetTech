// Get FAQ record
query "faq/{faq_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.faq_id
    } as $faq
  
    precondition ($faq != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $faq
  guid = "LjWSVqXac0qPoQ2do8cncFO9YIU"
}