NPI_testbed <- function( compArgs, progressFields ) {
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
  
  compArgs_base <- compArgs 
#  compArgs_base <- NPI:::checkRestartProgressAndPassword( compArgs )
  
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
    
    compArgs_file <- topconnect::appendFileMetadata( compArgs_file, filename, file_password="erlichda" ) # 'info' should be added to 'compArgs' here
    print( "append done")
    
    cases <- topconnect::caseIter( compArgs_file, 6 )
    print( "caseIter" )
    #    foreach::foreach(case = cases) %dopar% { # have the ability to do files in parallel as well as run futures (below)
    while ( cases$hasNext() ) {
      case <- cases$nextElem()
      print( case )
      compArgs_file$findClass('metadataInformer')$set( "case", case )
      # KLUGE! 'session' is currently not in a compositeArgument.
      # Perhaps a better solution is to make 'case' a compositeArgument and add it?
      compArgs_file$findClass('metadataInformer')$set( "session", case$UUID )
      
      progressStrings <- list(whereConditionString=topconnect:::createWhereConditionString(progressFields,compArgs_file), insertNames=paste0(names(progressFields),collapse=','), insertValues=topconnect:::createInsertValuesString(progressFields,compArgs_file) )
      
      cat( " : ", case$centerTime )
      idx <- idx + 1
      if ( idx > nbrWorkers ) {
        idx <- 1
      }
      processThisCase( case, compArgs_file, filename, progressStrings )
    } # cases$hasNext
    rm( compArgs_file)
    gc()
  } # fileProvider$hasNext
}

