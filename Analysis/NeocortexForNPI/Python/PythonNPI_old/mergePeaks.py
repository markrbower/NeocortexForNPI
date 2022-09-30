def mergePeaks(prev_peaks, peaks, CW):
    import numpy as np
    import pandas as pd

    if len(peaks) > 0:
        if len(prev_peaks) > 1:
            # Remove the olds
            T = peaks['time']
            minT = min(T)
            prev_T = prev_peaks['time']
            bad_idx = np.where(prev_T < (minT - CW))
            if len(bad_idx) > 0:
                prev_peaks = np.delete(prev_peaks, bad_idx)

            # Add the new
            if len(prev_peaks) > 0:
                prev_peaks = pd.concat([prev_peaks, peaks], ignore_index=False)
            else:
                prev_peaks = peaks
        else:
            prev_peaks = peaks

    return prev_peaks
