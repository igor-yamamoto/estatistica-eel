import numpy as np
import pandas as pd
from funcs import find_idx

class NormDistr:
    def __init__(self, media=0, var=1, n=1):
        self.media = media
        self.var = var
        self.n = n
        pass
        
    def tabela_norm(self):
        file_norm = 'distr/Norm.dat'
        out = pd.read_csv(file_norm)
        out.columns = ['Z', 'N(Z)']
        return out

    def valor_z_de_norm(self, norm_valor):
        out = self.tabela_norm()
        norm_table = out['N(Z)'].values
        idx_z = find_idx(norm_table, norm_valor)
        z_o = out['Z'][idx_z]
        return z_o

    def valor_norm_de_z(self, z_valor):
        out = self.tabela_norm()
        Z = out['Z'].values
        idx_norm = find_idx(Z, z_valor)
        norm_o = out['N(Z)'][idx_norm]
        return round(norm_o, 5)
    
    def IC(self, conf = 0.95, intervalo = 'bilateral'):
        out = self.tabela_norm()

        alp = 1 - conf
        
        if intervalo == 'bilateral':
            alp_meio = alp/2
            conf_meio = 0.5 - alp_meio
            
            z = self.valor_z_de_norm(conf_meio)

            C = z*np.sqrt(self.var/self.n)
            lim_inf = self.media - C
            lim_sup = self.media + C
        
        elif intervalo == 'unilateral superior':
            z = self.valor_z_de_norm(conf-0.5)

            C = z*np.sqrt(self.var/self.n)
            lim_inf = '-infinito'
            lim_sup = self.media + C
            
        elif intervalo == 'unilateral inferior':
            z = self.valor_z_de_norm(conf-0.5)

            C = z*np.sqrt(self.var/self.n)
            lim_inf = self.media - C
            lim_sup = 'infinito'

        return lim_inf, lim_sup
    
    
class StudentDistr:
    def __init__(self, media = 0, var = 1, n = 1):
        self.media = media
        self.var = var
        self.n = n
        pass
    
    def creat_map(self):
        head_map = np.array([.9, .8, .7, .6, .5, .4, .3, .2, .1, .09, .08, .07, .06, .05, .04, .03, .02, .01, .005, .002, .001])
        index_map = np.array([  2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,  11.,  12., 13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,  22.,  23., 24.,  25.,  26.,  27.,  28.,  29.,  30.,  35.,  40.,  50.,  60., 120.])
        return head_map, index_map
    
    def tabela_student(self):
        file_t = 'distr/Student.dat'
        student = pd.read_csv(file_t)
        return student

    def valor_t(self, conf, n, interval = 'bilateral'):
        student = self.tabela_student()

        alp = 1 - conf
        hd_map, index_map = self.creat_map()

        if interval == 'bilateral':
            p = alp
        elif interval == 'unilateral':
            p = 2*alp

        idx_p = find_idx(array = hd_map, x = p)
        idx_i = find_idx(array = index_map, x = n)
        t = student.iloc[idx_i, [idx_p+1]].values[0]

        return t
    
    def IC(self, conf = 0.95, intervalo = 'bilateral'):        
        if intervalo == 'bilateral':
            t = self.valor_t(conf, n = self.n, interval = 'bilateral')

            C = t*np.sqrt(self.var/self.n)
            lim_inf = self.media - C
            lim_sup = self.media + C
        
        elif intervalo == 'unilateral superior':
            t = self.find_t(conf, n = self.n, interval = 'unilateral')
            
            C = t*np.sqrt(self.var/self.n)
            lim_inf = '-infinito'
            lim_sup = X_med + C
            
        elif intervalo == 'unilateral inferior':
            t = self.find_t(conf, n = self.n, interval = 'unilateral')
            
            C = t*np.sqrt(self.var/self.n)
            lim_inf = X_med - C
            lim_sup = 'infinito'

        return round(lim_inf, 4), round(lim_sup, 4)
    
class XiDistr:
    def __init__(self, var = 1, n = 1):
        self.var = var
        self.n = n
        pass
    
    def xi_create_map(self):
        head_map = np.array([.99, .98, .975, .95, .90, .80, .70, .60, .50, .40, .30, .20, .10, .05, .04, .025, .02, .01, .002, .001])
        index_map = np.array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50.])
        return head_map, index_map

    def tabela_xi(self):
        file_xi = 'distr/Xi.dat'
        xi = pd.read_csv(file_xi)
        return xi

    def valor_q(self, conf, n, intervalo = 'bilateral'):
        xi = self.tabela_xi()
        
        alp = 1 - conf

        head_map, index_map = self.xi_create_map()
        idx_i = find_idx(index_map, n)

        if intervalo == 'bilateral':
            alp_meio = alp/2
            p1, p2 = 1 - alp_meio, alp_meio
            idx_q_1 = find_idx(head_map, p1)
            idx_q_2 = find_idx(head_map, p2)

            q1 = xi.iloc[idx_i, [idx_q_1+1]].values[0]
            q2 = xi.iloc[idx_i, [idx_q_2+1]].values[0]

            q = (q1, q2)
            
        elif intervalo == 'unilateral inferior':
            p = alp
            idx_q = find_idx(head_map, p)

            q = xi.iloc[idx_i, [idx_q+1]].values[0]
            q = (0, q)
            
        elif intervalo == 'unilateral superior':
            p = 1 - alp
            idx_q = find_idx(head_map, p)

            q = xi.iloc[idx_i, [idx_q+1]].values[0]
            q = (q, 'infty')

        return q
    
    def IC(self, conf = 0.95, intervalo = 'bilateral'):
        q1, q2 = self.valor_q(conf, self.n, intervalo = intervalo)

        if intervalo == 'unilateral inferior':
            lim_inf = ((self.n-1)*self.var**2)/q2
            lim_sup = 'infty'
        elif intervalo == 'unilateral superior':
            lim_inf = 0
            lim_sup = ((self.n-1)*self.var**2)/q1
        elif intervalo == 'bilateral':
            lim_inf = ((self.n-1)*self.var**2)/q2
            lim_sup = ((self.n-1)*self.var**2)/q1

        return lim_inf, lim_sup
