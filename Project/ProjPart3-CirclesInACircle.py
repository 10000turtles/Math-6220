from pyomo.opt import SolverFactory

import pyomo
import random

from pyomo.environ import *
from graphics import *


circRad = 1
circles = 12

trials = 100
best_value = circles

for tri in range(trials):

    model = ConcreteModel()

    model.rBound = Var(
        bounds=(0, 200), within=NonNegativeReals, initialize=circles)

    for i in range(circles):
        num = ceil(sqrt(circles))
        model.add_component(
            'x'+str(i), Var(within=Reals, initialize=(2*random.random()-1)*circles))
        model.add_component(
            'y'+str(i), Var(within=Reals, initialize=(2*random.random()-1)*circles))

        model.add_component(
            'Uboundx'+str(i), Constraint(expr=model.component('x'+str(i))**2 + model.component('y'+str(i))**2 <= (model.rBound - circRad)**2))

        # model.add_component('Lboundx'+str(i), Constraint(expr=-
        #                     model.component('x'+str(i)) + circRad <= 0))
        # model.add_component('Lboundy'+str(i), Constraint(expr=-
        #                     model.component('y'+str(i)) + circRad <= 0))

    for i in range(0, circles, 1):
        for j in range(i+1, circles, 1):
            model.add_component('dist'+str(i)+','+str(j), Constraint(expr=-(model.component('x'+str(i)) - model.component('x'+str(j)))**2 -
                                                                     (model.component('y'+str(i)) - model.component('y'+str(j)))**2 + (2*circRad)**2 <= 0))

    model.objective = Objective(expr=model.rBound, sense=minimize)

    # opt = SolverFactory('couenne')
    # opt.solve(model)

    opt = SolverFactory('mindtpy')
    results = opt.solve(model, mip_solver='glpk', nlp_solver='ipopt')

    if (value(model.rBound) < best_value):
        best_value = value(model.rBound)
        best_model = model

    if (tri % ceil(trials/100) == 0):
        print(f"{(tri/trials)*100}% Completed")


best_model.rBound.display()

win = GraphWin("My Circle", 1000, 1000)

for i in range(circles):

    scale = 500/value(best_model.rBound)
    c = Circle(
        Point(
            scale*(value(best_model.component('x'+str(i))) +
                   value(best_model.rBound)),
            scale*(value(best_model.component('y'+str(i)))+value(best_model.rBound))), scale*circRad)
    c.setFill("blue")
    c.draw(win)

c = Circle(Point(500, 500), 500)
c.draw(win)

win.getMouse()
