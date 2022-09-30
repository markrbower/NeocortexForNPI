import sys

import numpy as np
import pandas as pd
import igraph as ig
import leidenalg as la


def findGraphicalCommunities(case, variables, parms, CC):
    use_database = False
    cm = parms["computation_mask"]
    CW = parms["CW"]

    N = 0

    # Create the full graph
    cntr = 0
    if CC.shape[0] > 0:
        tmpCC = CC[['Tsource', 'Ttarget', 'weight']]
        tuples = [tuple(r) for r in tmpCC.to_numpy()]
        grph = ig.Graph.TupleList(tuples, edge_attrs='weight')

        uniqueTarget = np.unique(CC['Ttarget'])

        output = []
        N = len(uniqueTarget)
        subject = variables['subject']
        channel = variables['channel']
        clusterid = 0
        seizureUsed = int(case['centerTime'])
        UUID = case['UUID']

        for idx in np.arange(0, N):
            tCN = int(uniqueTarget[idx])
            sub_idx = [x for x in grph.vs if ((x['name'] >= (tCN - CW)) & (x['name'] <= tCN))]
            if len(sub_idx) > 1:  # The community is larger than just this node.
                # Sub-graph based on time.
                sub_grph = grph.subgraph(sub_idx)
                sub_cliques = la.find_partition(sub_grph, la.ModularityVertexPartition, weights=sub_grph.es['weight'])
                sub_cliques_membership = sub_cliques.membership
                tmp = [int(x) for x in list(sub_grph.vs['name'])]
                sub_idx = np.where(np.asarray(tmp) == tCN)[0][0]
                clusterid = sub_cliques_membership[sub_idx]
                member_idx = [i for i, x in enumerate(sub_cliques_membership) if x == clusterid]
                # Sub-graph based on membership
                grph_clique = sub_grph.subgraph(member_idx)
                edz_idx = [ig.Graph.incident(grph_clique, x) for x in grph_clique.vs.indices]
                edz = list([list(grph_clique.es[x]) for x in edz_idx])
                edz_ = list([list(np.unique(edz))])
                if len(edz_) > 0:
                    print(cntr)
                    enz = list()
                    incident = list()
                    weights = list()
                    for i in range(len(edz_)):
                        for j in range(len(edz_[i])):
                            edge = edz_[i][j]
                            if isinstance(edge, ig.Edge):
                                if hasattr(edge, 'source') & (edge['weight'] is not None):
                                    source_idx = edge.source
                                    enz.append(source_idx)
                                    incident.append(int(list(grph_clique.vs(source_idx))[0]['name']))
                                    weights.append(np.round(edge['weight'], 4))
                                else:
                                    print('stop')
                            elif isinstance(edge, list):
                                if len(edge) > 0:
                                    for k in range(len(edge)):
                                        edge_ = edge[k]
                                        if hasattr(edge_, 'source') & (edge_['weight'] is not None):
                                            source_idx = edge_.source
                                            enz.append(source_idx)
                                            incident.append(int(list(grph_clique.vs(source_idx))[0]['name']))
                                            weights.append(np.round(edge_['weight'], 4))
                                        else:
                                            print('stop')
                            else:
                                print('stop')

                    str_incident = ','.join(map(str, map(int, incident)))
                    str_weights = ','.join(map(str, weights))
                    cc_idx = np.where(CC['Ttarget'] == tCN)
                    tmp = list(CC['WVtarget'][cc_idx[0]])
                    waveform_str = ','.join(map(str,tmp[0]))

                    # database
                    if use_database:
                        cc_idx = np.where(CC['Ttarget'] == tCN)
                        waveform = CC['WVtarget'][cc_idx[0]]
                        waveform_str = ','.join(waveform)
#                        waveform = np.array(list(map(float, map(lambda x: x.strip(''), waveform_str.split(',')))))
                        abs_waveform = np.absolute(waveform)
                        peak_idx = np.where(abs_waveform == np.max(abs_waveform))
                        peakVal = abs_waveform[peak_idx[1]] * np.sign(waveform[cm[peak_idx[1]]])
                        energyVal = np.sqrt(sum(abs_waveform * abs_waveform))
                        result = pd.DataFrame(
                            {'subject': subject, 'channel': channel, 'time': tCN, 'waveform': waveform_str,
                             'clusterid': 0,
                             'seizureUsed': seizureUsed, 'peak': peakVal, 'energy': energyVal, 'incident': str_incident,
                             'weights': str_weights, 'UUID': UUID})
                        # dib$insert( result )

                    # data to pass forward
                    tmp = pd.DataFrame(
                        {'time': [str(int(tCN))], 'incident': [str_incident], 'weights': [str_weights], 'clusterid': [0],
                         'waveform': [waveform_str]})
                    if len(output)==0:
                        output = tmp
                    else:
                        output = pd.concat([output,tmp])
                    cntr = cntr + 1

    return output
