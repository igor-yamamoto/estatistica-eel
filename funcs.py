import numpy as np

def find_idx(array, x):
    idx = np.abs(array-x).argmin()
    return idx