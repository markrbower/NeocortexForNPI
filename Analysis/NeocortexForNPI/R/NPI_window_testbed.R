# NPI_window_testbed
# January 19, 2022
# Mark R. Bower
# Yale University
#
# The goal of this function is to wrap the parameters given as inputs into an argumentComposite variable, "compArgs".
#

# create table tasks (nodename varchar(128),path varchar(256),data varchar(64),institution varchar(64),lab varchar(32),experiment varchar(32),subject int(11),signaltype varchar(32),iterationtype varchar(32),label varchar(512) not null,centerTime bigint,done boolean,created timestamp default current_timestamp, modified timestamp default current_timestamp on update current_timestamp, primary key (label) );
#

NPI_window_testbed <- function(path,taskName,institution,lab,experiment,subject,signalType,centerTime,iterationType,hostname,dbName,db_user,db_password,file_password,range,minimum_sampling_frequency,waveform_mask,computation_mask,database_update_limit,filter_detect_lowF,filter_detect_highF,filter_keep_lowF,filter_keep_highF,correlationWindow,CCthreshold,EDthreshold,blackout) { 
  #' Run the Network Parameter Outlier (NPO) algorithm.
  #' 
  #' @export
  #' @examples
  #' \dontrun{
  #' }
  #
  compArgs <- RFactories::argumentComposite()
  dbp <- RFactories::databaseProvider(user=db_user,password=db_password,host=hostname,dbname=dbName)
  compArgs$add( dbp )
  if ( dir.exists('/data/Halo_data_from_Roni') ) {
    compArgs$add( RFactories::fileProvider(path='/data/Halo_data_from_Roni',iterationType='directory',pattern="*.mef") )
  } else if ( dir.exists('./data/Halo_data_from_Roni/mef2') ) {
      compArgs$add( RFactories::fileProvider(path='./data/Halo_data_from_Roni/mef2',iterationType='directory',pattern="*.mef",file_password=file_password) )
  } else {
    print( "Cannot find a directory for data" )
    return()
  }
  aInf <- RFactories::analysisInformer(experiment='NeuroVista',subject='11',centerTime=0,pattern="*.mef",lab="RNCP")
  compArgs$add( aInf )
  # Load the parameters from this command line, not a parameter file.
  parms <- c(minimum_sampling_frequency=32000,correlationWindow=unname(correlationWindow),blackout=unname(blackout),CCthreshold=unname(CCthreshold),EDthreshold=unname(EDthreshold),waveform_mask=unname(waveform_mask),computation_mask=unname(computation_mask),database_update_limit=100,filter_detect_lowF=unname(filter_detect_lowF),filter_detect_highF=unname(filter_detect_highF),filter_keep_lowF=unname(filter_keep_lowF),filter_keep_highF=unname(filter_keep_highF),signalType='AP')
  pInf <- RFactories::parameterInformer( parms )
  compArgs$add( pInf )
  #

  options(warn=-1)
  options(stringsAsFactors = FALSE);

  # Run the analysis
  T <- system.time( NPI_testbed( compArgs ) )
  
  # Store the parms and times to the database.
  conn <- DBI::dbConnect( RMySQL::MySQL(), user=db_user, password=password, host=hostname, dbname=dbName)
  query <- paste0( "insert into testbed_halo (subject,channel,cw,cc_threshold,user,sys,elapsed) values " )
  query <- paste0( query, "(\'", fdata$subject, "\',\'", fdata$channel, "\'," )
  query <- paste0( query, correlationWindow,",",CCthreshold,",",EDthreshold,",",blackout,",",T[1],",",T[2],",",T[3],");")
  DBI::dbGetQuery( conn, query )
  DBI::dbDisconnect( conn )
}
