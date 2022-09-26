import numpy as np
from collections import Counter


def assignClusterids(nodes, compArgs, counter):
    N = len(nodes)
    if N == 0:
        return nodes

    # Cluster the new nodes
    idxs = np.where(nodes['counter'] == counter)
    for idx in idxs:
        incident_times = nodes['incident'][idx].split(",")
        if len(incident_times) > 0:
            incident_idx = np.array(list(map(int, map(lambda x: np.where(nodes['time']) == x))))
            if len(incident_idx) > 0:
                clusterids = nodes['clusterid'][incident_idx]
                clusterids = clusterids[np.where(clusterids > 0)]
                if len(clusterids) > 0:
                    nodes['clusterid'][idx] = Counter(clusterids).most_common(1)[0][0]
            else:
                nodes['clusterid'][idx] = np.max(nodes['clusterid']) + 1
        else:  # This node is isolated from previous nodes. It has no input. It was only a source
            nodes['clusterid'][idx] = np.max(nodes['clusterid']) + 1

    #  save(file="parallelWindowNPO_2.RData",nodes)

    resultStrx = list(prev_nodes=nodes, persistIdxs=idxs)
    return resultStrx
