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
import random

from pyomo.environ import *
from graphics import *

circRad = 1
circles = 20

model = ConcreteModel()

model.xyBound = Var(
    bounds=(0, 200), within=NonNegativeReals, initialize=circles)

for i in range(circles):
    num = ceil(sqrt(circles))
    model.add_component(
        'x'+str(i), Var(within=NonNegativeReals, initialize=random.random()*circles))
    model.add_component(
        'y'+str(i), Var(within=NonNegativeReals, initialize=random.random()*circles))

    model.add_component(
        'Uboundx'+str(i), Constraint(expr=model.component('x'+str(i)) <= model.xyBound - circRad))
    model.add_component(
        'Uboundy'+str(i), Constraint(expr=model.component('y'+str(i)) <= model.xyBound - circRad))

    model.add_component('Lboundx'+str(i), Constraint(expr=-
                        model.component('x'+str(i)) + circRad <= 0))
    model.add_component('Lboundy'+str(i), Constraint(expr=-
                        model.component('y'+str(i)) + circRad <= 0))

for i in range(0, circles, 1):
    for j in range(i+1, circles, 1):
        model.add_component('dist'+str(i)+','+str(j), Constraint(expr=-(model.component('x'+str(i)) - model.component('x'+str(j)))**2 -
                                                                 (model.component('y'+str(i)) - model.component('y'+str(j)))**2 + (2*circRad)**2 <= 0))

model.objective = Objective(expr=model.xyBound, sense=minimize)

# opt = SolverFactory('couenne')
# opt.solve(model)

opt = SolverFactory('mindtpy')
opt.solve(model, mip_solver='glpk', nlp_solver='ipopt')

model.objective.display()
model.display()

# model.pprint()

win = GraphWin("My Circle", 1000, 1000)

for i in range(circles):

    scale = 1000/value(model.xyBound)
    c = Circle(
        Point(
            scale*value(model.component('x'+str(i))),
            scale*value(model.component('y'+str(i)))), scale*circRad)
    c.setFill("blue")
    c.draw(win)
win.getMouse()
model.display()
model.pprint()
