setupResultsDatabase <- function( compArgs, progressFields ) {
  #' @export
  library( DBI )
  library( RMySQL )
  
  hostname <- compArgs$get('host')
  if ( length(hostname) == 0 ) {
    hostname <- 'localhost'
  }
  dbName <- compArgs$get('dbname')
  if ( length(dbName) == 0 ) {
    hostname <- 'mysql'
  }
  db_user <- compArgs$get('user')
  if ( length(db_user) == 0 ) {
    db_user <- 'root'
  }
  password <- compArgs$get('password')
  if ( length(password) == 0 ) {
    password <- ''
  }
  print( paste0( "hostname: ", hostname ) )
  print( paste0( "password: ", password ) )

  conn <- DBI::dbConnect( RMySQL::MySQL(), user=db_user, password=password, host=hostname, dbName=dbName)

  query <- paste0( "CREATE DATABASE IF NOT EXISTS testbed_results;" )
  DBI::dbGetQuery( conn, query )
  
  query <- paste0( "USE testbed_results;" )
  DBI::dbGetQuery( conn, query )
  
  query <- paste0( "CREATE TABLE IF NOT EXISTS testbed_halo (subject varchar(32), channel varchar(32), cw int, CCthreshold float, EDthreshold float, blackout float, user float, sys float, elapsed float);" )
  DBI::dbGetQuery( conn, query )
  
  # Progress
  query <- namedListToCreateQuery( "progress", progressFields, c(done="tinyint(1)") )
  print( paste0( "setupResultsDatabase: ", query ) )
  DBI::dbGetQuery( conn, query )
  
  DBI::dbDisconnect( conn )
  
  NeocortexForNPI:::createBaseNPItestbedTables( dbName="testbed_results", hostname=hostname, password=password )

#  populateBehaviorTablesForTestbed( dbName="testbed_results", hostname=hostname, password=password )
}
