'''We compute the ap for the first few primes of the
elliptic curve defined by the function equation'''
#%%
def elliptic_curve(coeff, x, y):
    '''
    coeffs=[a_1, a_2, a_3, a_4, a_5, a_6]
    y^2 + a_1*xy + a_3y =
      x^3 + a_2x^2 + a_4x+ a_6
    '''
    a1, a2, a3, a4, a6 = coeff
    return y**2 + a1*x*y + a3*y - \
      (x**3 + a2*x**2 + a4*x+ a6)  #elliptic curve y^2=x^3+1

def discriminant(coeffs):
    '''
    Given coeffs=[a1, a2, a3, a4, a6],
    we compute the discriminant of the elliptic curve
    using the formulas in 
    Cremona Ch3
    '''
    a1, a2, a3, a4, a6 = coeffs

    b2=a1**2 + 4*a2
    b4=a1*a3 + 2*a4
    b6=a3**2 + 4*a6
    b8=a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2
    
    disc = -b2**2*b8 - 8*b4**3-27*b6**2 + 9*b2*b4*b6
    return disc


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
    for n, an in a:
        print(an, n, an*(n**(-s)))
        sum+=an*(n**(-s))
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
