import numpy as np
import pandas as pd

def import_norm_table():
    file_norm = '../auc_norm_table.dat'
    out = pd.read_csv(file_norm)
    Z = out['x'].to_numpy()
    norm = out['auc'].to_numpy()
    return Z, norm

def find_idx(array, x):
    idx = np.abs(array-x).argmin()
    return idx

def find_Z_from_norm(Z, norm_table, norm_value):
    idx_z = find_idx(norm_table, norm_value)
    z_o = Z[idx_z]
    return z_o

def find_norm_from_Z(Z, norm_table, z_value):
    idx_norm = find_idx(Z, z_value)
    norm_o = norm_table[idx_norm]
    return norm_o


