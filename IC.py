import numpy as np
import pandas as pd

def IC(X_med, n, sigma, conf):
    from norm import import_norm_table
    Z, norm = import_norm_table()

    alp = 1 - conf
    alp_meio = alp/2
    conf_meio = 0.5 - alp_meio

    from norm import find_idx
    idx_z = find_idx(norm, conf_meio)
    z = Z[idx_z]

    from math import sqrt
    C = z*sigma/sqrt(n)
    lim_inf = X_med - C
    lim_sup = X_med + C

    return lim_inf, lim_sup

def IC_st(X_med, n, S, conf):
    from student import import_student_table, find_t
    st = import_student_table()

    t = find_t(st, conf, n, interval = 'bilateral')
    print(t)
    from math import sqrt
    C = t*S/sqrt(n)
    lim_inf = X_med - C
    lim_sup = X_med + C

    return lim_inf, lim_sup

def IC_st_unilateral(X_med, n, S, conf, uni = 'superior'):
    from student import import_student_table, find_t
    st = import_student_table()

    t = find_t(st, conf, n, interval = 'unilateral')
    print(t)
    from math import sqrt
    if uni == 'superior':
        lim_sup = X_med + t*S/sqrt(n)
        lim = ('-infty', lim_sup)
    elif uni == 'inferior':
        lim_inf = X_med - t*S/sqrt(n)
        lim = (lim_inf, 'infty')

    return lim

def IC_xi(n, S, conf, interval = 'bilateral'):
    from xi import find_q
    q1, q2 = find_q(conf, n, interval = interval)

    if interval == 'unilateral inferior':
        lim_inf = ((n-1)*S**2)/q2
        lim_sup = 'infty'
    elif interval == 'unilateral superior':
        lim_inf = 0
        lim_sup = ((n-1)*S**2)/q1
    elif interval == 'bilateral':
        lim_inf = ((n-1)*S**2)/q2
        lim_sup = ((n-1)*S**2)/q1

    return lim_inf, lim_sup
