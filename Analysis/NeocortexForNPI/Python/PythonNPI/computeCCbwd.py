import numpy as np
import pandas as pd
from withinWindow import withinWindow
from applyPeaksToCor import applyPeaksToCor
from applyPeaksToER import applyPeaksToER
from itertools import chain
from makeIterable import makeIterable


def computeCCbwd(parms, peaks, startIdx):
    # import numpy as np
    # import pandas as pd
    #
    # This section allows the user to create a test dataset
    if False:
        x = np.random.rand(5, 3)
        v = {'time': x.tolist()}
        peaks = pd.DataFrame(v, columns=['voltage'], index=[0, 3, 8, 16, 18])

    cm = parms['computation_mask']
    CW = parms['CW']

    cc_threshold = parms['cc_threshold']
    er_threshold = parms['er_threshold']

    compute_idx = np.arange(startIdx, len(peaks))
    if len(compute_idx) > 0:
        times = np.asarray(peaks['time'])
        # Remember that peaks is N rows, each containing an Nsample-element list
        IDX_source = [withinWindow(times, x, CW) for x in times]
        LL = [len(x) for x in IDX_source]
        IDX_target = [[x] * LL[x] for x in np.arange(0, len(LL))]

        # Flatten lists
        IDX_source = [item for sublist in IDX_source for item in sublist]
        IDX_target = [item for sublist in IDX_target for item in sublist]

        voltage = [np.asarray(tmp.split(','), dtype=int) for tmp in peaks['voltage']]
        Vsource = [voltage[x] for x in IDX_source]
        Vtarget = [voltage[x] for x in IDX_target]

        # Compute
        cc_all = np.asarray([np.corrcoef(x, y)[0][1] for x, y in zip(Vsource, Vtarget)])
        er_all = np.asarray([np.sum(x * x) / np.sum(y * y) for x, y in zip(Vsource, Vtarget)])
        # Create the return data frame
        # V = ["".join(["%.1f," % i for i in peaks[x]]) for x in np.arange(0, len(peaks))]

        Ttarget = times[IDX_target]
        Tsource = times[IDX_source]
        # Keep the valid values
        gt_cc = np.where(np.asarray(cc_all) >= cc_threshold)[0]
        lt_er = np.where(np.asarray(er_all) <= 1 / er_threshold)[0]
        gt_er = np.where(np.asarray(er_all) >= er_threshold)[0]
        keepIdx = np.intersect1d(np.intersect1d(gt_cc, gt_er), lt_er)
        #    keepIdx <- which( cc_all > cc_threshold )
        Ttarget = np.round(Ttarget[keepIdx])  # This is a weird problem of text-to-numeric at large values.
        Tsource = np.round(Tsource[keepIdx])  # This is a weird problem of text-to-numeric at large values.
        Vtarget = [Vtarget[x] for x in keepIdx]
        Vsource = [Vsource[x] for x in keepIdx]
        weight = cc_all[keepIdx]

        dx = {"Tsource": Tsource, "WVsource": Vsource, "Ttarget": Ttarget, "WVtarget": Vtarget, "weight": weight}
        CC = pd.DataFrame(dx)
        return CC
    else:
        return NULL
