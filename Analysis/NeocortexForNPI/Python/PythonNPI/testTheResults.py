import numpy as np
from collections import Counter
from plotClusterWaveforms import plotClusterWaveforms


def testTheResults(L, output, idx_big_clusters=None):
  table_clusterid = Counter(output['clusterid'])
  # Are all waveforms in a cluster from the same source?
  all_counts = np.fromiter(table_clusterid.values(), dtype=int)
  idx_big_clusters <- np.where( all_counts > 5 )
  IDs = (table_clusterid[idx_big_clusters]).names()
  for clusterid in IDs:
    idx = np.where( output['clusterid'] == clusterid )
    table_predicted = Counter(output['clusterid'][idx])
    predicted = table_predicted[np.where(table_predicted.names()==clusterid)]
    table_actual = Counter( L[idx] )
    actual = table_actual[np.where(table_actual.names()==clusterid)]
    pct = 100.0 * predicted[1] / actual[1]

    print( ": ".join( ( clusterid, pct ) ) )
    plotClusterWaveforms(output,clusterid)

  # Do any waveforms from a cluster get assigned to low-count clusters or NA?
  for src in np.arange(1,4):
    clusterids = output['clusterid'][ np.where( L == src ) ]
    print( ": ".join(src) )
#    print( table(clusterids ) )

#    cat( crayon::bgGreen( crayon::red( "Not all caategories were found.\n" ) ) )
