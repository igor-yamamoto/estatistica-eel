import numpy as np
import pandas as pd

def xi_create_map():
    head_map = np.array([.99, .98, .975, .95, .90, .80, .70, .60, .50, .40, .30, .20, .10, .05, .04, .025, .02, .01, .002, .001])
    index_map = np.array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50.])
    return head_map, index_map

def import_xi_table():
    file_xi = '../distr/Xi.dat'
    xi = pd.read_csv(file_xi)
    return xi

def find_q(conf, n, interval = 'bilateral'):
    xi = import_xi_table()

    from norm import find_idx
    alp = 1 - conf

    head_map, index_map = xi_create_map()
    idx_i = find_idx(index_map, n-1)

    if interval == 'bilateral':
        alp_meio = alp/2
        p1, p2 = 1 - alp_meio, alp_meio
        idx_q_1 = find_idx(head_map, p1)
        idx_q_2 = find_idx(head_map, p2)

        q1 = xi.iloc[idx_i, [idx_q_1+1]].values[0]
        q2 = xi.iloc[idx_i, [idx_q_2+1]].values[0]

        q = (q1, q2)
    elif interval == 'unilateral inferior':
        p = 1 - alp
        idx_q = find_idx(head_map, p)

        q = xi.iloc[idx_i, [idx_q+1]].values[0]
        q = (0, q)
    elif interval == 'unilateral superior':
        p = alp
        idx_q = find_idx(head_map, p)

        q = xi.iloc[idx_i, [idx_q+1]].values[0]
        q = (q, 'infty')

    return q
