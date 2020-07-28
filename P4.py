import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def tabela_ANOVA_raw(X, Y):
    n = len(Y)
    unique_vals = np.unique(X)

    k = len(unique_vals)
    vals = np.zeros([3, k])

    m = 0
    for i in unique_vals:
        Y_grupo = Y[np.argwhere(X == i)]
        vals[0, m] = Y_grupo.mean()
        vals[1, m] = (Y_grupo.mean())**2
        vals[2, m] = len(Y_grupo)
        m += 1

    PT1 = (vals[1, :]*vals[2, :]).sum()
    PT2 = (Y**2).sum()
    PT3 = len(Y)*(Y.mean())**2

    SQEn, SQDen, SQTot = PT1 - PT3, PT2 - PT1, PT2 - PT3
    QMEn, QMDen, QMTot = SQEn/(k-1), SQDen/(n-k), SQTot/(n-1)

    F = QMEn/QMDen

    SQ = [SQEn, SQDen, SQTot]
    QM = [QMEn, QMDen, QMTot]

    print_ANOVA(n, k, SQ)

def tabela_ANOVA_from_table(table):
    ni, k = table.shape
    n = ni*k

    yi_ = table.mean()
    y_ = yi_.mean()
    yij2 = table**2

    PT1 = (ni*yi_**2).sum()
    PT2 = yij2.sum().sum()
    PT3 = n*y_**2

    SQEn, SQDen, SQTot = PT1-PT3, PT2-PT1, PT2-PT3
    SQ = [SQEn, SQDen, SQTot]

    print_ANOVA(n, k, SQ)


def print_ANOVA(n, k, SQ):

    QMEn, QMDen, QMTot = SQ[0]/(k-1), SQ[1]/(n-k), SQ[2]/(n-1)
    QM = [QMEn, QMDen, QMTot]

    F = QMEn/QMDen

    print("-------------------------------")
    print("TABELA ANOVA")
    print("-------------------------------")
    print("Fonte de Variação (FV) / Graus de liberdade (GL) / Soma Quadratica (SQ) / Quadrado medios (QM) / F observado")
    print("Entre: " + str(k-1) + " / " + str(SQ[0]) + " / " + str(QM[0]) + " / " + str(F))
    print("Dentro: " + str(n-k) + " / " + str(SQ[1]) + " / " + str(QM[1]))
    print("Total: " + str(n-1) + " / " + str(SQ[2]) + " / " + str(QM[2]))


def alpha_beta(data, args):
    n = data.shape[0]
    
    x = args[0]
    y = args[1]
    
    x_mean = data[x].mean()
    y_mean = data[y].mean()

    xy = (table[x]*table[y]).sum()
    x2 = (table[x]**2).sum()
    
    beta_ch = ((n*x_mean*y_mean)-xy)/(n*x_mean**2-x2)
    alpha_ch = y_mean - beta_ch*x_mean
    return alpha_ch, beta_ch

def ANOVA_regr(data, args):
    n = data.shape[0]
    x = args[0]
    y = args[1]
    
    x_mean = data[x].mean()
    y_mean = data[y].mean()
    
    alpha_ch, beta_ch = alpha_beta(table, args)
    y_ch = alpha_ch + data[x]*beta_ch
    
    SQTot = ((data[y]-y_mean)**2).sum()
    SQRes = ((data[y]-y_ch)**2).sum()
    SQReg = ((y_ch-y_mean)**2).sum()
    
    QMReg = SQReg
    QMRes = SQRes/(n-2)
    QMTot = SQTot/(n-1)
    
    Fobs = QMReg/QMRes
    
    ANOVA_regr = pd.DataFrame({'n': [1, n-2, n-1],
                               'SQ': [SQReg, SQRes, SQTot],
                              'QM': [QMReg, QMRes, QMTot],
                              'F': [Fobs, Fobs, Fobs]
                             }, index = ['Regressão', 'Resíduo', 'Total'])
    
    return ANOVA_regr


def IC_regr(data, args, t, Se, const='beta', x_ext = None):
    x = data[args[0]]
    y = data[args[1]]
    
    x_mean = x.mean()
    n = len(x)
    
    alpha_ch, beta_ch = alpha_beta(table, args)
    
    if const == 'beta':
        c = beta_ch
        C = t*Se*np.sqrt(1/((x-x_mean)**2).sum())
    if const == 'alpha':
        c = alpha_ch
        x2 = (x**2).sum()
        C = t*Se*np.sqrt(x2/(((x-x_mean)**2).sum()*n))
    if const == 'IP':
        c = alpha_ch + beta_ch*x_ext
        xdiff = ((x-x_mean)**2).sum()
        C = t*Se*np.sqrt(1+(1/n)+((x_ext-x_mean)**2/xdiff))
    
    return c-C, c+C