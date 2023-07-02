def LHS(y):
    return 3*y**2+3*y

def RHS(x):
    return 2*x**3 + 3*x**2 + x

for x in range(0,1000):
    for y in range(0, 1000000):
        if LHS(y)==RHS(x):
            print(x,y)

''' For x in range(0, 1000) and y
in range(0,1000000) 
the only solutions are
(0,0)
(1,1)
(5,10)
(6,13)
(85, 645)'''