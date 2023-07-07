#%%
with open('primes.txt') as file:
    data=file.read()


# %%
primes=[int(i) for i in data[:-1].split('\n')]

# %%
a=[]
def equation(x,y):
    return y**2-x**3-1
#%%
for p in primes[:300]:
    count=0
    print(p)
    for i in range(0,p):
        for j in range(0,p):
           if equation(i,j) % p ==0:
               #print(i,j)
               count+=1
    print((p,p-count))
    a.append((p, p-count))

        
# %%
def L_fcn(a,s):
    sum=1
    for p, ap in a:
        print(ap, p, ap*(p**(-s)))
        sum+=ap*(p**(-s))
    return sum
# %%
