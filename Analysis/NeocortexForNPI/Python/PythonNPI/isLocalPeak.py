def isLocalPeak(c_, data, mask):
    import numpy as np

    # Must ensure that a complete waveform can be retrieved by "mask",
    # even if the peak requires the maximum shift.
    flag = False
    max_shift = 5
    idx = c_ + mask
    bad = np.where(idx < max_shift | idx > (len(data) - max_shift))
    if len(bad) == 0:
        check = data[idx]
        # A local peak is "sovereign" for it's polarity;
        # i.e., it is still a "peak" even if the subsequent "valley" is deeper.
        if data[c_] >= 0:
            if data[c_] >= max(check):
                flag = True
        else:
            if data[c_] <= min(check):
                flag = True

    return flag
