def separateSignalFromNoise( output, rateThreshold ):
  counts <- table( table( output$clusterid ) )

  # Scale the firing rate so that the highest-rate cluster fires at 1 Hz
  duration <- max( output$time ) - min( output$time )
  nbrOfMembers <- as.numeric( names( counts) )
  scaleFactor <- duration / max(nbrOfMembers)
  threshold <- 0.01 * duration / scaleFactor  # Firing rate in Hz
  
  idx_signal <- which( nbrOfMembers > threshold )
  signalClusterNames <- which( table(output$clusterid) %in% names(counts)[idx_signal] )
  return( signalClusterNames )


