# import pyomo.environ as pyo
# from pyomo.opt import SolverFactory

# def ObjRule(m):
#     return m.x1 #3*m.x1**4-4*m.x1**3-12*m.x1**2 + 3*m.x2**4-4*m.x2**3-12*m.x2**2

# model = pyo.ConcreteModel(name="Nonconvex MINLP sample")

# model.x1 = pyo.Var(domain=pyo.Integers, bounds=(-5, 5), initialize=-1)
# model.x2 = pyo.Var(domain=pyo.Integers, bounds=(-5, 5), initialize=-1)

# model.OBJ = pyo.Objective(rule = ObjRule, sense = pyo.minimize)

# opt = pyo.SolverFactory('couenne')
# res = opt.solve(model)

# print(f"\nObjective: {model.OBJ()}")
# print(f"x1: {model.x1()}")
# print(f"x2: {model.x2()}")

from pyomo.opt import SolverFactory

import pyomo

from pyomo.environ import *

model = ConcreteModel()

model.x = Var(bounds=(1.0,10.0),initialize=5.0)
model.y = Var(within=Binary)

model.c1 = Constraint(expr=(model.x-4.0)**2 - model.x <= 50.0*(1-model.y))
model.c2 = Constraint(expr=model.x*log(model.x)+5.0 <= 50.0*(model.y))

model.objective = Objective(expr=model.x, sense=minimize)

SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt', tee=True) 

model.objective.display()
model.display()
model.pprint()