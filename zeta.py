#%%
import numpy as np 

#%%
MAX_N=1000000
def zeta(s):

    if s.real>1:
        return zeta_right_of_1(s)
    elif s.real>0:
        return zeta_right_of_0(s)
    else:
        raise NotImplementedError(f'{s}<=0 not yet implemented')


def zeta_right_of_1(s):
    if s.real>1:
        sum=0
        for i in range(1,MAX_N):
            sum+=i**(-s)
        return sum
    else:
        raise ValueError


#%%
def zeta_right_of_0(s):
    if s.real>0:
        sum_even=0
        sum_odd=0
        
        for i in range(1,MAX_N, 2):
            sum_odd+=i**(-s)
        for i in range(2,MAX_N, 2):
            sum_even+=i**(-s)
        print(s.imag)
        zeta_s=(sum_odd-sum_even)/(1-2**(1-s))
        #zeta_file.write(f'{s} {zeta_s} \n ')
        return zeta_s
    else:
        raise ValueError(f'real part of s={s} must be larger than 0')



# %%
if __name__=='__main__':
    with open('zeta50-1.csv', 'w') as zeta_file:
        s=0.5 + 1j*np.arange(0, 50, 0.1)
        zeta_values=(np.vectorize(zeta))(s)



#
