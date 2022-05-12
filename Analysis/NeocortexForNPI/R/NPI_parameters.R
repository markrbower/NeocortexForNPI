NPI_parameters <- function(...) {
  # Run by a docker container
  # Start a network and MySQL container named "mysql-server", first.
  #' @export
  
  args <- list(...)
  
  # Files converted from .ncs by "convertHaloData.R"
  library( DBI )
  library( RMySQL )

  # Find data
  #print( "Looking for files" )
  mefFiles <- list.files("/data/Halo_data_from_Roni",pattern="*.mef",full.names=TRUE)
  if ( length(mefFiles)== 0 ) {
    mefFiles <- list.files("./data/Halo_data_from_Roni/mef2",pattern="*.mef",full.names=TRUE)
  }
  L <- length( mefFiles )
  print( paste0( L, " files to process." ) )
  
  # Set parameter grid (window duration, CC threshold,  ) for software test
  # CW <- c(300E6,60E6)
  # CC <- c(0.8,0.9)
  # ED <- c(1.2,1.5)
  # BO <- c(50E3,10E3)
  # save(CW,CC,ED,BO,file='parameters.RData')
  load(file='/mnt/parameters.RData')

  # for real
  parms <- expand.grid( CW=CW, CC=CC,ED=ED,BO=BO )
  L <- nrow(parms)

  # Loops
#  apply( parms, 1, function(x) NPO_window_byParm(x) )
#  print( "Going into NPO_window_byParm" )
#  NPO_window_byParm( parms ) # for software test

  correlationWindow = parms$duration
  CCthreshold = parms$threshold

  hostname <- RFactories:::parseArg( args, 'hostname' )
  if ( length(hostname) == 0 ) {
    hostname <- 'localhost'
  }
  dbName <- RFactories:::parseArg( args, 'dbName' )
  if ( length(dbName) == 0 ) {
    hostname <- 'mysql'
  }
  db_user <- RFactories:::parseArg( args, 'db_user' )
  if ( length(db_user) == 0 ) {
    db_user <- 'root'
  }
  password <- RFactories:::parseArg( args, 'password' )
  if ( length(password) == 0 ) {
    password <- ''
  }
  
  #print( L )
  for ( idx in seq(1,L) ) {
      NPI_window_testbed(path='/data/Halo_data_from_Roni', taskName='preprocessing', institution='Yale', lab='RCNP', experiment='Halo_test', subject='11', signalType='AP', centerTime=0, iterationType='directory', hostname=hostname, dbName=dbName, db_user=db_user, db_password='secret', file_password='erlichda', range=c(-1000,1000), minimum_sampling_frequency=20000,waveform_mask=list(seq(-6,25)),computation_mask=list(seq(3,15)),database_update_limit=100,filter_detect_lowF=600,filter_detect_highF=6000,filter_keep_lowF=600,filter_keep_highF=6000,correlationWindow=parms$CW[idx],CCthreshold=parms$CC[idx],EDthreshold=parms$ER[idx],blackout=parms$BO[idx])
  }
  
}

