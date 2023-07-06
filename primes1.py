#%%
import numpy as np

primes=[2]

for n in range(3, 5000):
    i=0
    p=primes[i]
    n_is_prime=1
    while p<=np.sqrt(n):
        if n%p ==0:
            #print(f'n={n}, p={p}, primes={primes}')
            n_is_prime=0
            break
        i+=1
        p=primes[i]

    if n_is_prime==1:
        primes.append(n)


with open('primes.txt', 'w') as file:
    file.writelines([str(p)+ '\n' for p in primes])
# %%
