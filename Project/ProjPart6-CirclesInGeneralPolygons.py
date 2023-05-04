from pyomo.opt import SolverFactory

import pyomo
import random
import math

from pyomo.environ import *
from graphics import *


circRad = 1
circles = 2

trials = 1
best_value = 10000

smidge = 0.02

x_and_y = [(1, 0), (-1/2, 1/2), (0, 0), (-1/2, -1/2)]
sides_of_polygon = len(x_and_y)

print(x_and_y)
abct = []
deF = []


for i in range(sides_of_polygon):
    x_1 = x_and_y[i][0]
    y_1 = x_and_y[i][1]

    x_2 = x_and_y[(i+1) % sides_of_polygon][0]
    y_2 = x_and_y[(i+1) % sides_of_polygon][1]

    a = y_2 - y_1
    b = x_1 - x_2
    c = -y_2*b - x_2*a

    d = 2*(x_1-x_2)
    e = 2*(y_1-y_2)
    f = y_2**2 - y_1**2 + x_2**2 - x_1**2

    theta = (smidge + 2*(i+1/2)*math.pi/sides_of_polygon) % (2*math.pi)

    is_leq = (theta < math.pi) and (theta > 0)

    abct.append((a, b, c, is_leq))
    deF.append((d, e, f))

print(abct)

for tri in range(trials):

    model = ConcreteModel()

    model.rBound = Var(
        bounds=(1, 200), within=NonNegativeReals, initialize=10)

    for i in range(circles):
        num = ceil(sqrt(circles))
        model.add_component(
            'x'+str(i), Var(within=Reals, initialize=(random.random()*2-1)))
        model.add_component(
            'y'+str(i), Var(within=Reals, initialize=(random.random()*2-1)))

        for j in range(sides_of_polygon):
            a = abct[j][0]
            b = abct[j][1]
            c = abct[j][2]

            d = deF[j][0]
            e = deF[j][1]
            f = deF[j][2]

            leq = abct[j][3]

            p1 = x_and_y[i]
            p2 = x_and_y[(i+1) % sides_of_polygon]

            T = 30000

            model.add_component(f"ub_tog{i}_{j}_rect_1", Var(
                within=NonNegativeReals, initialize=0))
            model.add_component(f"ub_tog{i}_{j}_rect_2", Var(
                within=NonNegativeReals, initialize=0))
            model.add_component(f"ub_tog{i}_{j}_rect_c", Var(
                within=NonNegativeReals, initialize=0))
            model.add_component(f"ub_tog{i}_{j}_circ", Var(
                within=NonNegativeReals, initialize=0))

            # model.add_component(f"ub_tog{i}_{j}_circ_1", Constraint())
            # model.add_component(f"ub_tog{i}_{j}_circ_2", Constraint())

            model.add_component(f"ub_tog{i}_{j}_rect_1_check", Constraint(expr=(a*model.component('x'+str(
                i)) + b*model.component('y'+str(i)) + model.rBound*c)**2 >= -model.component(f"ub_tog{i}_{j}_rect_1") + a ** 2+b ** 2))

            model.add_component(f"ub_tog{i}_{j}_rect_2_check", Constraint(expr=(d*model.component('x'+str(
                i)) + e*model.component('y'+str(i)) + model.rBound*f)**2 >= -model.component(f"ub_tog{i}_{j}_rect_2") + (model.rBound**2)*(b**2 + a**2)*(d**2 + e**2)/4))

            model.add_component(f"ub_tog{i}_{j}_rect_check", Constraint(
                expr=model.component(f"ub_tog{i}_{j}_rect_2")*model.component(f"ub_tog{i}_{j}_rect_1") <= model.component(f"ub_tog{i}_{j}_rect_c")))

            model.add_component(
                f'Uboundx{i}_{j}', Constraint(
                    expr=a*model.component('x'+str(i)) + b*model.component('y'+str(i)) + model.rBound*c <= T*(1-model.component(f"ub_tog{i}_{j}_rect_c")) - sqrt(a ** 2+b ** 2)))

        model.add_component(
            'Uboundcirc'+str(i), Constraint(expr=model.component('x'+str(i))**2 + model.component('y'+str(i))**2 <= (model.rBound - circRad)**2))

    for i in range(0, circles, 1):
        for j in range(i+1, circles, 1):
            model.add_component('dist'+str(i)+','+str(j), Constraint(expr=-(model.component('x'+str(i)) - model.component('x'+str(j)))**2 -
                                                                     (model.component('y'+str(i)) - model.component('y'+str(j)))**2 + (2*circRad)**2 <= 0))

    def obj_rule(model):
        obj = model.rBound

        # for i in range(circles):
        #     for j in range(sides_of_polygon):
        #         obj = obj + \
        #             T*model.component(f"ub_tog{i}_{j}_rect_c") + \
        #             T*model.component(f"ub_tog{i}_{j}_circ")

        return obj

    model.objective = Objective(
        rule=obj_rule, sense=minimize)

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

for i in range(sides_of_polygon):
    s = Line(Point(scale*x_and_y[i][0] + scale, scale*x_and_y[i][1] + scale), Point(scale*x_and_y[(
        i+1) % sides_of_polygon][0] + scale, scale*x_and_y[(i+1) % sides_of_polygon][1] + scale))
    s.draw(win)

c = Circle(Point(500, 500), 500)
c.draw(win)

win.getMouse()
