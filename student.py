import numpy as np
import pandas as pd

def creat_map():
    head_map = np.array([.9, .8, .7, .6, .5, .4, .3, .2, .1, .09, .08, .07, .06, .05, .04, .03, .02, .01, .005, .002, .001])
    index_map = np.array([  2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,  11.,  12., 13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,  22.,  23., 24.,  25.,  26.,  27.,  28.,  29.,  30.,  35.,  40.,  50.,  60., 120.])
    return head_map, index_map

def import_student_table():
    file_t = 'distr/Student.dat'
    student = pd.read_csv(file_t)
    return student

def find_t(conf, n, interval = 'bilateral'):
    student = import_student_table()

    from norm import find_idx
    alp = 1 - conf
    hd_map, index_map = creat_map()

    if interval == 'bilateral':
        p = alp
    elif interval == 'unilateral':
        p = 2*alp

    idx_p = find_idx(hd_map, p)
    idx_i = find_idx(index_map, n)
    t = student.iloc[idx_i, [idx_p+1]].values[0]

    return t

