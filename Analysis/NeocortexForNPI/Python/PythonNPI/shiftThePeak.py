def shiftThePeak(x, mask, raw_data):
    import numpy as np

    # Return the shifted mask indices
    max_shift = 5
    check_idx = x + np.arange(-max_shift, max_shift)
    center_idx = max_shift + 1
    if raw_data[x] >= 0:
        peak_idx = raw_data[check_idx].argmax()
        shift = peak_idx - center_idx
    else:
        valley_idx = raw_data[check_idx].argmin()
        shift = valley_idx - center_idx

    new_idx = shift + x + mask
    return raw_data[new_idx]
