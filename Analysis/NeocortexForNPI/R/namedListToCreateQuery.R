namedListToCreateQuery <- function( table, dynamicFields, fixedFields ) {
  # Dynamic and fixed field lists are split so that other functions can access
  # just one or the other.
  query <- paste0( "create table if not exists ", table )
  notFirstFlag = FALSE
  for ( name in names(dynamicFields) ) {
    if ( notFirstFlag ) {
      query <- paste0( query, ", ", name, " ", dynamicFields[name] )
    } else {
      query <- paste0( query, " ( ", name, " ", dynamicFields[name] )
      notFirstFlag = TRUE
    }
  }
  for ( name in names(fixedFields) ) {
    if ( notFirstFlag ) {
      query <- paste0( query, ", ", name, " ", fixedFields[name] )
    } else {
      query <- paste0( query, " ( ", name, " ", fixedFields[name] )
      notFirstFlag = TRUEs
    }
  }
  if ( notFirstFlag ) {
    query <- paste0( query, " );" )
  } else {
    query <- paste0( query, ";" )
  }
  return( query )
}
