import numpy as np


def applyPeaksToER(peaks, x, y):
    v1 = [np.asarray(tmp.split(','), dtype=int) for tmp in peaks['voltage'][x]]
    v2 = [np.asarray(tmp.split(','), dtype=int) for tmp in peaks['voltage'][y]]
    er = [(np.sum(x * x) / np.sum(y * y)) for x, y in zip(v1, v2)]
    return er
