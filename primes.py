#%%
import numpy as np
from pathlib import Path


#%%
def is_prime(n, primes=[2]):
    if n>1 and isinstance(n, int):
        root_n=np.floor(np.sqrt(n))
        i=0
        l=len(primes)
        p=primes[i]
        while p <= root_n:
            if n % p ==0:
                return False
            i+=1
            if i<l:
                p=primes[i]
            else:
                primes.append()
        return True
    
#%%
def find_primes(d=100, primes=[2], filename='primes.csv'):
    p=primes[-1]
    print(f'p={p}')
    print(f'd={d}')
    for i in range(p,p+d):
        
            primes.append(i)
            print(i)

    with open(filename, 'a') as file:
        file.writelines([str(i) for i in primes])
#%%
if __name__=='__main__':
    FILE=Path('primes.csv')
    if FILE.is_file():
        print('yes')
        with open(FILE, 'r') as file:
            data=file.read()
            data_split=data.split()
            primes=[int(i) for i in data_split]
    else:
        primes=[2]
        print('here')
        with open(FILE, 'w') as file:
            file.writelines([str(i) for i in primes])

    find_primes(d=100, primes=primes, filename=FILE)



# %%
