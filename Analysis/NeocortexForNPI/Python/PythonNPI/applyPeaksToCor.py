import numpy as np


def applyPeaksToCor(peaks, x, y):
    v1 = [np.asarray(tmp.split(','), dtype=int) for tmp in peaks['voltage'][x]]
    v2 = [np.asarray(tmp.split(','), dtype=int) for tmp in peaks['voltage'][y]]
    cc = [np.corrcoef(x, y)[0][1] for x, y in zip(v1, v2)]
    return cc
