import numpy as np
from scipy.optimize import linprog
import itertools
 
def flatten(l):
    return [item for sublist in l for item in sublist]

def findsubsets(s, n):
    return list(itertools.combinations(s, n))
 

value = [15,13,14,17,17,14,16,12,19,10,13,14,17,16,13,14,12,18,15,16]
sizes = [11,12,13,14,15,16,17,18,19,10,11,12,13,14,15,16,17,18,19,10]

b = 30

obj = np.array(value)

A = np.array([sizes])
c = np.array([b])

perms = flatten([findsubsets(range(20), n) for n in range(1,4,1)])

for i in perms:
    if sum([sizes[q] for q in i]) > b:
        
        base = np.zeros(20)
        for j in i:
            base[j] = base[j] + 1

        A = np.append(A,[base],0)

        c = np.append(c,2)

# print(A.shape)

A = np.append(A,[np.ones(20)],0)
c = np.append(c,2)

# Negative objective function to get max
res = linprog(-obj,A_ub = A, b_ub = c,bounds = [(0,1) for i in range(20)] ,method='highs')

for i in range(len(res.x)):
    if res.x[i]>0:
        print(str(res.x[i]) + " of object: " + str(i+1) + " (value: " + str(value[i]) + ", size: " + str(sizes[i]) + ")")

print("total value: " + str(-res.fun))
 