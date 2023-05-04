from pyomo.opt import SolverFactory

import pyomo
import random
import math

from pyomo.environ import *
from graphics import *


circRad = 1
circles = 12

trials = 5
best_value = 10000

smidge = 0.02

x_and_y = [(0, 1), (0, 0)]

circle_bounds = 10

for i in range(circle_bounds):
    x_and_y.append((cos(i*2*math.pi/circle_bounds/4),
                   sin(i*2*math.pi/circle_bounds/4)))

sides_to_regular_polygon = len(x_and_y)

print(x_and_y)
abct = []

for i in range(sides_to_regular_polygon):
    x_1 = x_and_y[i][0]
    y_1 = x_and_y[i][1]

    x_2 = x_and_y[(i+1) % sides_to_regular_polygon][0]
    y_2 = x_and_y[(i+1) % sides_to_regular_polygon][1]

    a = y_2 - y_1
    b = x_1 - x_2
    c = -y_2*b - x_2*a
    theta = (smidge + 2*(i+1/2)*math.pi/sides_to_regular_polygon) % (2*math.pi)

    is_leq = (theta < math.pi) and (theta > 0)

    abct.append((a, b, c, is_leq))

print(abct)

for tri in range(trials):

    model = ConcreteModel()

    model.rBound = Var(
        bounds=(1, 200), within=NonNegativeReals, initialize=10)

    for i in range(circles):
        num = ceil(sqrt(circles))
        model.add_component(
            'x'+str(i), Var(within=Reals, initialize=random.random()))
        model.add_component(
            'y'+str(i), Var(within=Reals, initialize=random.random()))

        for j in range(sides_to_regular_polygon):
            a = abct[j][0]
            b = abct[j][1]
            c = abct[j][2]
            leq = abct[j][3]

            # if leq:
            model.add_component(
                f'Uboundx{i}_{j}', Constraint(
                    expr=a*model.component('x'+str(i)) + b*model.component('y'+str(i)) + model.rBound*c <= -sqrt(a ** 2+b ** 2)))
            # else:
            #     model.add_component(
            #         f'Uboundx{i}_{j}', Constraint(
            #             expr=a*model.component('x'+str(i)) + b*model.component('y'+str(i)) + model.rBound*c <= -sqrt(a ** 2+b ** 2)))

            # model.add_component(
            #     f'Uboundx{i}_{j}', Constraint(
            #         expr=a*model.component('x'+str(i)) + b*model.component('y'+str(i)) + model.rBound*c >= 0))
        model.add_component(
            'Uboundcirc'+str(i), Constraint(expr=model.component('x'+str(i))**2 + model.component('y'+str(i))**2 <= (model.rBound - circRad)**2))

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

best_model.display()

win = GraphWin("My Circle", 1000, 1000)

scale = 500/value(best_model.rBound)

for i in range(circles):
    print(f"(x_{i},y_{i}) = ({value(best_model.component('x'+str(i)))},{value(best_model.component('y'+str(i)))})")

    c = Circle(
        Point(
            scale*(value(best_model.component('x'+str(i))) +
                   value(best_model.rBound)),
            scale*(value(best_model.component('y'+str(i)))+value(best_model.rBound))), scale*circRad)
    c.setFill("blue")
    c.draw(win)

scale = 500

for i in range(sides_to_regular_polygon):
    s = Line(Point(scale*x_and_y[i][0] + scale, scale*x_and_y[i][1] + scale), Point(scale*x_and_y[(
        i+1) % sides_to_regular_polygon][0] + scale, scale*x_and_y[(i+1) % sides_to_regular_polygon][1] + scale))
    s.draw(win)

c = Circle(Point(500, 500), 500)
c.draw(win)

win.getMouse()
