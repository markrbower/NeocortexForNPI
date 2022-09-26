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
        times = peaks['time']
        # Remember that peaks is N rows, each containing an Nsample-element list
        IDX_source = [withinWindow(times, x, CW) for x in times]
        LL = [len(x) for x in IDX_source]
        IDX_target = [[x] * LL[x] for x in np.arange(0, len(LL))]

        # Compute
        cc_all = [applyPeaksToCor(peaks, x, y) for x, y in zip(IDX_source, IDX_target)]
        er_all = [applyPeaksToER(peaks, x, y) for x, y in zip(IDX_source, IDX_target)]
        # Create the return data frame
        # V = ["".join(["%.1f," % i for i in peaks[x]]) for x in np.arange(0, len(peaks))]

        # Flatten the lists
        IDX_target = list(chain.from_iterable([makeIterable(x) for x in IDX_target]))
        IDX_source = list(chain.from_iterable([makeIterable(x) for x in IDX_source]))

        Ttarget = times[IDX_target].to_numpy()
        WVtarget = peaks['voltage'][IDX_target].to_numpy()
        Tsource = times[IDX_source].to_numpy()
        WVsource = peaks['voltage'][IDX_source].to_numpy()
        # Flatten lists
        cc_all = np.asarray([item for sublist in cc_all for item in sublist])
        er_all = np.asarray([item for sublist in er_all for item in sublist])
        # Keep the valid values
        gt_cc = np.where(cc_all >= cc_threshold)[0]
        lt_er = np.where(er_all <= 1/er_threshold)[0]
        gt_er = np.where(er_all >= er_threshold)[0]
        keepIdx = np.intersect1d(np.intersect1d(gt_cc, gt_er), lt_er)
        #    keepIdx <- which( cc_all > cc_threshold )
        Ttarget = np.round(Ttarget[keepIdx])  # This is a weird problem of text-to-numeric at large values.
        WVtarget = WVtarget[keepIdx]
        Tsource = np.round(Tsource[keepIdx])  # This is a weird problem of text-to-numeric at large values.
        WVsource = WVsource[keepIdx]
        weight = cc_all[keepIdx]

        dx = {"Tsource": Tsource, "WVsource": WVsource, "Ttarget": Ttarget, "WVtarget": WVtarget, "weight": weight}
        CC = pd.DataFrame(dx)
        return CC
    else:
        return NULL
