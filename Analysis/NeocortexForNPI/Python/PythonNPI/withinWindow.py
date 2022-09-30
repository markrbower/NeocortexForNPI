import numpy as np


def withinWindow(v, t, t_):
    print(t)
    g1 = np.where(v >= (t - t_))[0]
    g2 = np.where(v < t)[0]
    idx = np.intersect1d(g1, g2)
    return idx
