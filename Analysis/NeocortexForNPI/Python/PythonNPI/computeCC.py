from computeCCbwd import computeCCbwd


def computeCC(parms, peaks, t0):
    import numpy as np
    import pandas as pd

    # Default and check
    CC = pd.DataFrame()  # How BIG a dataframee?!
    if len(peaks) > 0:
        T = peaks['time']
        # Which peaks should be considered "targets"?
        v = np.where(T >= t0)[0]
        if len(v) > 0:
            CC = computeCCbwd(parms, peaks, v[0])
        else:
            print("No new peaks")

    # This should be a dataframe, unlike the input.
    # It must include clusterid for "prev_peak" entries.
    return CC
