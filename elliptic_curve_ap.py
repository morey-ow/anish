'''We compute the ap for the first few primes of the
elliptic curve defined by the function equation'''
#%%
def equation(x,y):
    return y**2-x**3-1  #elliptic curve y^2=x^3+1

def compute_ap(number_of_primes=100):
    '''compute ap's
    for the first 100 primes'''
    a=[]
    for p in primes[:number_of_primes]:
            count=0
            print(p)
            for i in range(0,p):
                for j in range(0,p):
                    if equation(i,j) % p ==0:
                        #print(i,j)
                        count+=1
            ap=p-count
            print((p,ap))
            a.append((p, ap))
    return a
    

# %%
def L_fcn(a,s):
    '''
    This function computes the L-series
    at s given by coefficients in a 
    list specified by a
    assuming Dirichlet series converges at s
    '''
    sum=1
    for p, ap in a:
        print(ap, p, ap*(p**(-s)))
        sum+=ap*(p**(-s))
    return sum
# %%
if __name__=='__main__':
    with open('primes.txt') as file:
        data=file.read()
    global primes
    primes=[int(i) for i in data[:-1].split('\n')]
    a=compute_ap(number_of_primes=100)
    print(L_fcn(a, 1))
# %%
