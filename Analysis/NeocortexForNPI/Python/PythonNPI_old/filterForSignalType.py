def filterForSignalType(variables, buffer, data):
    import numpy as np
    import scipy.signal as signal

    bufferSize = len(buffer)
    skipSize = 1

    # Load the data into the buffer
    # What to do when data size is (perhaps much!) smaller than buffer size?
    padSize = min(round((bufferSize - len(data)) / 2), np.floor(len(data) / 2))
    buffer[0:padSize] = np.flip(data[0:padSize])
    dataIdx = np.arange(0, len(data))
    buffer[dataIdx + padSize] = data
    padIdx = np.arange((padSize + len(data)), min((len(data) + 2 * padSize), len(buffer)))
    dataIdx = np.arange((len(data) - len(padIdx)), len(data))
    buffer[padIdx] = np.flip(data[dataIdx])

    filt_buffer = signal.filtfilt(variables['detect_b'], variables['detect_a'], buffer)
    dataIdx = np.arange(padSize, (padSize + len(data)), skipSize)
    filt_data_detect = filt_buffer[dataIdx]

    # Load the data into the buffer
    padSize = min(round((bufferSize - len(data)) / 2), np.floor(len(data) / 2))
    buffer[0:padSize] = np.flip(data[1:padSize])
    dataIdx = np.arange(0, len(data))
    buffer[dataIdx + padSize] = data
    padIdx = np.arange((padSize + len(data) + 1), min((len(data) + 2 * padSize), len(buffer)))
    dataIdx = np.arange((len(data) - len(padIdx) + 1), len(data))
    buffer[padIdx] = np.flip(data[dataIdx])

    # - Use higher-frequencies for actual data.
    filt_buffer = signal.filtfilt(variables['keep_b'], variables['keep_a'], buffer)
    dataIdx = np.arange(padSize, (padSize + len(data)), skipSize)
    filt_data_keep = filt_buffer[dataIdx]

    filteredData = {"filt_data_detect": filt_data_detect, "filt_data_keep": filt_data_keep,
                    "s0": data['s0'], "t0": data['t0'], "dt": data['dt']}
    # print( "Returning")
    return filteredData
