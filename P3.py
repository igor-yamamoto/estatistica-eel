import numpy as np

def Z_pop(p1_, n1, p2_, n2, D = 0):
    ## Aqui, pn_ sao as poprocoes AMOSTRAIS, enquanto D e a diferenca entre as proporcoes POPULACIONAIS

    zo = (p1_-p2_-D)/np.sqrt((p1_*(1-p1_)/n1)+(p2_*(1-p2_)/n2))

    return zo

def media_var(X):
    S2 = np.sum((X-X.mean())**2)/(len(X)-1)

    return X.mean(), S2

def Sc2(S1, n1, S2, n2, S = 'variancia'):
    if S == 'desvio padrao':
        S1, S2 = S1**2, S2**2

    Sc = ((n1-1)*S1+(n2-1)*S2)/(n1+n2-2)

    return Sc
