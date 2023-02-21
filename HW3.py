import numpy as np
from scipy.optimize import linprog
import itertools

key = np.eye(5,dtype=int)
resMat = np.eye(5)

count = 0
for i in range(4):
    for j in range(i+1,5,1):
        key[i][j] = count 
        count = count + 1


obj = np.array([3,7,2,8,2,9,8,7,1,2])

A = np.array([[0,0,0,0,0,0,0,0,0,0]])

b = np.array([0])

iteration = 1

while(True):
    

    res = linprog(-obj,A_ub = A, b_ub = b,bounds = [(0,1) for i in range(10)])

    count = 0
    for i in range(4):
        for j in range(i+1,5,1):
            resMat[i][j] = res.x[count] 
            count = count + 1
            
    print("\item Iteration: " + str(iteration))
    count = 0
    addedConst = False
    for i in range(3):
        for j in range(i+1,4,1):
            for k in range(j+1,5,1):    
                if resMat[i,j] + resMat[j,k] + resMat[i,k] > 2:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([2])

                    lhs[0,key[i,j]] = 1
                    lhs[0,key[j,k]] = 1
                    lhs[0,key[i,k]] = 1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)
                    
                    count = count + 1

                    print("\item Added constraint $x_{" + str(i+1) +str(j+1) + "} + x_{"  + str(i+1) +str(k+1) + "} + x_{" + str(j+1) +str(k+1) + "} \leq 2$") 
                
                if resMat[i,j] - resMat[j,k] - resMat[i,k] > 0 and not addedConst:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([0])

                    lhs[0,key[i,j]] = 1
                    lhs[0,key[j,k]] = -1
                    lhs[0,key[i,k]] = -1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)

                    count = count + 1

                    print("\item Added constraint $x_{" + str(i+1) +str(j+1) + "} - x_{"  + str(i+1) +str(k+1) + "} - x_{" + str(j+1) +str(k+1) + "} \leq 0$") 
                    addedConst = True
                if resMat[j,k] - resMat[i,j] - resMat[i,k] > 0 and not addedConst:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([0])

                    lhs[0,key[i,j]] = -1
                    lhs[0,key[j,k]] = 1
                    lhs[0,key[i,k]] = -1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)

                    count = count + 1

                    print("\item Added constraint $x_{" + str(j+1) +str(k+1) + "} - x_{"  + str(i+1) +str(j+1) + "} - x_{" + str(i+1) +str(k+1) + "} \leq 0$") 
                    addedConst = True
                if  resMat[i,k] - resMat[j,k] - resMat[i,j] > 0 and not addedConst:
                    lhs = np.array([[0,0,0,0,0,0,0,0,0,0]])
                    rhs = np.array([0])

                    lhs[0,key[i,j]] = -1
                    lhs[0,key[j,k]] = -1
                    lhs[0,key[i,k]] = 1

                    A = np.append(A,lhs,0)
                    b = np.append(b,rhs)

                    count = count + 1

                    print("\item Added constraint $x_{" + str(i+1) +str(k+1) + "} - x_{"  + str(j+1) +str(k+1) + "} - x_{" + str(i+1) +str(j+1) + "} \leq 0$") 
                    addedConst = True
    if(count == 0):
        print("\item No constraints added")
        break
    
    iteration = iteration + 1

print(res.x)
print(-res.fun)

