// Delete CARTAOTOKNZD record.
query "cartaotoknzd/{cartaotoknzd_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int cartaotoknzd_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.cartaotoknzd_id
    }
  }

  response = null
  guid = "196eYJpxfrPR1i1pat2aKv1KNIo"
}