import numpy as np
import pandas as pd

# 1. Set parameters
# 1.a. NPI parameters
from computeCC import computeCC
from findGraphicalCommunities import findGraphicalCommunities
from mergePeaks import mergePeaks

parms = {'cc_threshold': 0.85, 'er_threshold': 0.5, 'CW': 2000,
         'firingRateThreshold': 0.01, 'blackout': 4, 'computation_mask': [1, 2, 3, 4, 5, 6, 7]}
# 1.b. Parameters for adding variability and drift
N = 10000  # Total number of waveforms
SD = 5  # Std Dev of noise to be added to template waveforms
DRIFT_MAG = 2.0
DRIFT_CNT = 200
# 1.c. Filter properties
peakComputationVariables = {"subject": 1, "channel": "CSC1", "bandpassFilterFrequency_High": 6000, "bandpassFilterFrequency_Low": 600}

# 1.d. Define the Message Window; i.e., number of samples per block
MW = 20000

# 2. CREATE TOY DATA
# 2.a. Templates for four clusters, including a "noise" cluster
m = [[0, 5, 20, -30, -50, 0, 0],
     [0, -5, -20, 30, 50, 20, 0],
     [0, 10, 50, -120, -100, -80, -40],
     [0, 0, 0, 0, 0, 0, 0]]
s0 = 0
t0 = 0
dt = 1
# 2.b. Generate "noised" versions of templates with unequal frequencies.
T = np.cumsum(np.random.poisson(lam=5, size=N) + parms['blackout'])
L = np.random.choice([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], N) - 1
D = np.zeros([N, 7], dtype=int)
for idx in np.arange(0, N):
    D[idx] = m[L[idx]] + np.random.normal(loc=0, scale=SD, size=7)
# 2.c. Add drift to cluster 2
idx2 = np.asarray(np.where(L == 2)).ravel()
length2 = idx2.size
begin_drift_idx = idx2[round(length2 / 2)]
changed_idx = np.where(idx2 >= begin_drift_idx)[0]
# 2.c.1 Change the data during the drift
drift_idx = changed_idx[0:DRIFT_CNT]
idx_start = drift_idx[0]
multiplier = (((DRIFT_MAG - 1.0) / DRIFT_CNT) * np.arange(DRIFT_CNT) + 1)
D[idx2[drift_idx]] = D[idx2[drift_idx]] * multiplier[:, None]
# 2.c.1 Change the data after the drift until the end
drifted_idx = np.setdiff1d(changed_idx, drift_idx)
# idx_end = drift_idx[DRIFT_CNT]
D[idx2[drifted_idx]] = DRIFT_MAG * D[idx2[drifted_idx]]
# 2.d Package the data into a dataframe to merge time and voltage data
# 2.d.1 Convert matrix to a list-of-lists by rows
Dlist = list()
for row in D:
    tmp = ",".join(['%d' % num for num in row])
    Dlist.append(tmp)

# 2.d.2 Merge time and voltage to make a dataframe
N = len(T)
data = pd.DataFrame({'time': T, 'voltage': Dlist, 's0': [s0] * N, 't0': [t0] * N, 'dt': [dt] * N},
                    columns=['time', 'voltage', 's0', 't0', 'dt'])

# 2.e Compute "message" breaks
messages = list()
t = T[0]
while t <= T[N - 1]:
    idx = np.where((T >= t) & (T < (t + MW)))
    tmp = {'idx': list(T[idx]), 'centerTime': 0, 'UUID': 123}
    messages.append(tmp)
    t = t + MW


# 3. Implement the "Network Properties Identifier" (NPI) algorithm
# 3.a Define helper functions
def which(lst, a):
    return [i for i, x in enumerate(lst) if x == a]  # Remember, Python indices start at 0


# 3.b Loop through the messages
cntMessages = 0
prev_nodes = pd.DataFrame()
prev_peaks = pd.DataFrame()
if len(messages) > 0:
    # 3.b.1 Prime the pre, _, and post messages, along with output values
    iter_messages = iter(messages)
    message_pre = list()
    message = next(iter_messages)
    message_post = next(iter_messages, None)
    CC_next = []
    output = []
    cntMessage = 0
    while message_post is not None:
        cntMessage = cntMessage + 1
        # 3.b.2 Find the rows within 'data' to be analyzed
        dataIdxMessage = np.where(np.in1d(data['time'], message['idx']))[0]
        T = np.asarray(data['time'])[dataIdxMessage]
        voltage = np.asarray(data['voltage'])[dataIdxMessage]
        dataIdxBoth = np.where(np.in1d(data['time'], message['idx'] + message_post['idx']))[0]
        # 3.c The bulk of the NPI algorithm occurs here in four steps:
        #    1. Find peaks in the data
        #    2. Compute CC as edge weights
        #    3. Find local communities with graph clustering algorithms
        #    4. Find global labels by walking sequentially through the local results
        # 3.c.2 Compute CC for nodes "backward" of the current peak
        #
        # Start of a GPU pipeline here?
        # 3.c.1 Find peaks in the data
        # GOAL: peaks = pd.DataFrame(peak_matrix.tolist(), columns=['voltage'], index=T)
        # In my test case, this has already been done;
        # the peaks are the rows in data.
        #        peaks = computePeaks(peakComputationVariables, data)
        peaks = pd.DataFrame({'time': T, 'voltage': voltage})
        prev_peaks = mergePeaks(prev_peaks, peaks, parms['CW'])

        t0 = min(peaks['time'])
        CC = computeCC(parms, prev_peaks, t0)
        #        result = computeCC(CW, cc_threshold, er_threshold, cntMessage - 1, message, voltage,
        #                           data[dataIdxBoth]['time'], data[dataIdxBoth]['voltage'])
        # CC = pd.concat([CC_next, result], ignore_index=True, sort=False)

        # 3.c.3 Graph processing steps
        # Only find communities for the targets.
        nodes = findGraphicalCommunities(message_post, peakComputationVariables, parms, CC)

        message_pre = message
        message = message_post
        message_post = next(iter_messages, None)



