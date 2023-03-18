import numpy as np
from scipy.optimize import linprog
import itertools

key = np.eye(10,dtype=int)
resMat = np.eye(10)

count = 0
for i in range(9):
    for j in range(i+1,10,1):
        key[i][j] = count 
        count = count + 1


obj = np.array([1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1])

A = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

b = np.array([0])

iteration = 1

while(True):
    

    res = linprog(-obj,A_ub = A, b_ub = b,bounds = [(0,1) for i in range(45)])

    count = 0
    for i in range(9):
        for j in range(i+1,10,1):
            resMat[i][j] = res.x[count] 
            count = count + 1
    print("\item Iteration: " + str(iteration))
    count = 0
    addedConst = False
    for i in range(8):
        for j in range(i+1,9,1):
            for k in range(j+1,10,1):    
                if resMat[i,j] + resMat[j,k] - resMat[i,k] > 1:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([1])

                    lhs[0,key[i,j]] = 1
                    lhs[0,key[j,k]] = 1
                    lhs[0,key[i,k]] = -1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)
                    
                    count = count + 1

                    print("\item Added constraint $x_{" + str(i+1)+", " +str(j+1) + "} + x_{"  + str(j+1)+", " +str(k+1) + "} - x_{" + str(i+1)+", " +str(k+1) + "} > 1$") 
                
                if resMat[i,j] - resMat[j,k] + resMat[i,k] > 1:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([1])

                    lhs[0,key[i,j]] = 1
                    lhs[0,key[j,k]] = -1
                    lhs[0,key[i,k]] = 1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)

                    count = count + 1

                    print("\item Added constraint $x_{" + str(i+1)+", " +str(j+1) + "} - x_{"  + str(j+1)+", " +str(k+1) + "} + x_{" + str(i+1)+", " +str(k+1) + "} > 1$") 
                if  - resMat[i,j] + resMat[j,k] + resMat[i,k] > 1:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([1])

                    lhs[0,key[i,j]] = -1
                    lhs[0,key[j,k]] = 1
                    lhs[0,key[i,k]] = 1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)

                    count = count + 1

                    print("\item Added constraint $-x_{" + str(i+1)+", " +str(j+1) + "} + x_{"  + str(j+1)+", " +str(k+1) + "} + x_{" + str(i+1)+", " +str(k+1) + "} > 1$") 
                    
    if(count == 0):
        print("\item No constraints added")
        break
    
    iteration = iteration + 1

print(res.x)
print(-res.fun)

