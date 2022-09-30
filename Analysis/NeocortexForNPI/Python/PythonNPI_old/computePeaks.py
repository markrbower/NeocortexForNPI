from filterForSignalType import filterForSignalType
from isLocalPeak import isLocalPeak
from shiftThePeak import shiftThePeak


def computePeaks(variables, data):
    import numpy as np
    import pandas as pd

    # 1. Get dimensions and initialize variables
    n = len(data)
    m = len(data[1]['voltage'])
    peak_matrix = np.zeros((0, m))
    if n > 1:
        # 2. Filter the data. The following function returns two results:
        #   - 'detect' is filtered to promote detection by the computer
        #   - 'keep' is filtered to look correct to a human observer
        filteredData = filterForSignalType(variables, variables['buffer'], data)
        fdata = filteredData["filt_data_detect"]
        # 3. Find peaks by computing derivatives as finite differences.
        # 3.a. Peaks occur where changes in value change sign.
        dw = np.diff(fdata)
        sdw = np.sign(dw)
        dsdw = np.diff(sdw)
        C = np.nonzero(dsdw)
        C = C[0]
        # 3.b. Remove those at the boundary. A kluge, but this simplifies things.
        C = C[np.where((C > abs(min(variables['blackout_mask']))) |
                       (C < (len(C) - max(variables['blackout_mask']))))]
        if len(C) > 0:
            peak_matrix = np.zeros((len(C), m))
            T = np.zeros(len(C))
            idx = np.zeros(0, len(C))
            cnt = 0
            for c in C:
                # 3.c. Find those peaks that are "sovereign local peaks"; i.e., biggest in the window
                idx[cnt] = isLocalPeak(c, data, variables['blackout_mask'])
                # 3.d. Shift each local peak so that all peaks align on the same window index.
                peak_matrix[cnt] = shiftThePeak(idx[cnt], variables['waveform_mask'], fdata)
                T[cnt] = data[C]['time']
                cnt = cnt + 1

    # peaks are stored as pandas dataframes made from lists of waveforms indexed by timestamps
    peaks = pd.DataFrame(peak_matrix.tolist(), columns=['voltage'], index=T)
    return peaks
