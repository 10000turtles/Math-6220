import numpy as np
from scipy.optimize import linprog
import itertools



A = np.array([[-1,2],[5,1],[-2,-2],[1,1],[4,1]])

b = np.array([4,20,-7,6,16])

res = linprog(-pi,A_ub = A, b_ub = b,method='highs')

print("total value: " + str(-res.fun))
print("x value: " + str(res.x))