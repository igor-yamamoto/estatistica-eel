import numpy as np

from student import *

def nu(S1, S2, n1, n2, S = 'variancia'):
    if S == 'desvio_padrao':
        S1, S2 = S1**2, S2**2

    nu_val = ((S1/n1)+(S2/n2))**2/(((S1/n1)**2/(n1-1))+((S2/n2)**2/(n2-1)))

    return nu_val
