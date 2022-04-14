NPI_testbed <- function( compArgs ) {
  # Network Pattern Identifier
  #
  #' @export
  library(future)
  NPI:::setOptions()
  nbrWorkers <- 1
  plan(multisession,workers=nbrWorkers) # "multisession" is portable, "multicore" is not
  nbrFutures = round(1.5 * nbrWorkers)
#  p_limit <- 0
  p_limit <-  nbrWorkers + round( ( nbrFutures - nbrWorkers ) / 2 )
  
  futs <- vector( "list", nbrWorkers )
  for ( idx in seq(1,nbrWorkers) ) { futs[[idx]] <- future::future(1) }
  
  compArgs_base <- NPI:::checkRestartProgressAndPassword( compArgs )
  CW <- compArgs$get( 'correlationWindow' )
  bufferSizePower <- 24
  compArgs_base$findClass('analysisInformer')$add( list(bufferSize=2^bufferSizePower) )
  correlationWindow <- compArgs_base$get('correlationWindow')
  fileProvider <- compArgs_base$findClass( 'fileProvider' )
  idx <- 0
  while ( fileProvider$hasNext() ) {
    filename <- fileProvider$nextElem()
    compArgs_file <- createPtable( compArgs_base, filename )
    print( filename )
    compArgs_file <- topconnect::appendFileMetadata( compArgs_file, filename ) # 'info' should be added to 'compArgs' here
    cases <- topconnect::caseIter( compArgs_file, 6 )
    #    foreach::foreach(case = cases) %dopar% { # have the ability to do files in parallel as well as run futures (below)
    while ( cases$hasNext() ) {
      case <- cases$nextElem()
      compArgs_file$findClass('metadataInformer')$set( "case", case )
      cat( " : ", case$centerTime )
      idx <- idx + 1
      if ( idx > nbrWorkers ) {
        idx <- 1
      }
      # Gate
      val <- future::value( futs[[idx]] )
#      futs[[idx]] <- future::future( processThisCase( case, compArgs_file, filename ) )
      processThisCase( case, compArgs_file, filename )
    } # cases$hasNext
    rm( compArgs_file)
    gc()
  } # fileProvider$hasNext
  v <- future::value( db_future ) # Wait for the previous write to finish
  plan( sequential )
}

