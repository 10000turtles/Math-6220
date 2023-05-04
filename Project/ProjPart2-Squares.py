from pyomo.opt import SolverFactory

from pyomo.opt import SolverStatus, TerminationCondition

import pyomo
import random
import sys
import os

from pyomo.environ import *
from graphics import *

squares = 2

is_feasible = False

while (not is_feasible):
    model = ConcreteModel("Squares")

    model.tolerance = Var(bounds=(0.005, 0.005), initialize=0.005)

    model.xyBound = Var(
        bounds=(1.5, 200), within=NonNegativeReals, initialize=10)

    for i in range(squares):
        for j in range(4):
            model.add_component(
                f"c{j}_{i}_x", Var(within=NonNegativeReals, initialize=random.random()*squares))
            model.add_component(
                f"upper_bound_c{j}_{i}_x", Constraint(expr=model.component(f"c{j}_{i}_x") <= model.xyBound))
            model.add_component(f"lower_bound_c{j}_{i}_x", Constraint(expr=-
                                                                      model.component(f"c{j}_{i}_x") <= 0))
            model.add_component(
                f"c{j}_{i}_y", Var(within=NonNegativeReals, initialize=random.random()*squares))
            model.add_component(
                f"upper_bound_c{j}_{i}_y", Constraint(expr=model.component(f"c{j}_{i}_y") <= model.xyBound))
            model.add_component(f"lower_bound_c{j}_{i}_y", Constraint(expr=-
                                                                      model.component(f"c{j}_{i}_y") <= 0))
    for i in range(squares):
        for j in range(4):
            model.add_component(
                f"dist_c{j}_c{(j+1)%4}_{i}", Constraint(expr=(model.component(f"c{j}_{i}_x") - model.component(f"c{(j+1)%4}_{i}_x"))**2 + (model.component(f"c{j}_{i}_y") - model.component(f"c{(j+1)%4}_{i}_y"))**2 == 1))
        model.add_component(
            f"dist_c{0}_c{2}_{i}", Constraint(expr=(model.component(f"c{0}_{i}_x") - model.component(f"c{2}_{i}_x"))**2 + (model.component(f"c{0}_{i}_y") - model.component(f"c{2}_{i}_y"))**2 >= 1.99))
        model.add_component(
            f"dist_c{1}_c{3}_{i}", Constraint(expr=(model.component(f"c{1}_{i}_x") - model.component(f"c{3}_{i}_x"))**2 + (model.component(f"c{1}_{i}_y") - model.component(f"c{3}_{i}_y"))**2 >= 1.99))

    T = 100000
    for i in range(squares):
        for j in range(squares):
            if not j == i:
                for k in range(4):
                    for q in range(4):
                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_x", Var(
                            within=NonNegativeReals, initialize=random.random()))
                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_y", Var(
                            within=NonNegativeReals, initialize=random.random()))
                        model.add_component(f"b1_s{i}_c{k}_{j}_{q}", Var(
                            initialize=random.random()))
                        model.add_component(f"b2_s{i}_c{k}_{j}_{q}", Var(
                            initialize=random.random()))
                        model.add_component(f"m1_s{i}_c{k}_{j}_{q}", Var(
                            initialize=random.random()))
                        model.add_component(f"m2_s{i}_c{k}_{j}_{q}", Var(
                            initialize=random.random()))

                        x_1 = model.component(f"c{k}_{i}_x")
                        y_1 = model.component(f"c{k}_{i}_y")

                        x_2 = model.component(f"c{(k+1)%4}_{i}_x")
                        y_2 = model.component(f"c{(k+1)%4}_{i}_y")

                        x_3 = model.component(f"c{q}_{j}_x")
                        y_3 = model.component(f"c{q}_{j}_y")

                        x_4 = model.component(f"c{(q+1)%4}_{j}_x")
                        y_4 = model.component(f"c{(q+1)%4}_{j}_y")

                        m_1 = model.component(f"m1_s{i}_c{k}_{j}_{q}")
                        m_2 = model.component(f"m2_s{i}_c{k}_{j}_{q}")

                        b_1 = model.component(f"b1_s{i}_c{k}_{j}_{q}")
                        b_2 = model.component(f"b2_s{i}_c{k}_{j}_{q}")

                        Tol = model.tolerance

                        model.add_component(f"m1_s{i}_c{k}_{j}_{q}_valid_leq", Constraint(
                            expr=model.component(f"m1_s{i}_c{k}_{j}_{q}") <= Tol + (y_2 - y_1)/(x_2 - x_1)))

                        model.add_component(f"m2_s{i}_c{k}_{j}_{q}_valid_leq", Constraint(
                            expr=model.component(f"m1_s{i}_c{k}_{j}_{q}") <= Tol + (y_4 - y_3)/(x_4 - x_3)))

                        model.add_component(f"b1_s{i}_c{k}_{j}_{q}_valid_leq", Constraint(
                            expr=model.component(f"b1_s{i}_c{k}_{j}_{q}") <= Tol - m_1*x_1 + y_1))

                        model.add_component(f"b2_s{i}_c{k}_{j}_{q}_valid_leq", Constraint(
                            expr=model.component(f"b2_s{i}_c{k}_{j}_{q}") <= Tol - m_2*x_3 + y_3))

                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_x_valid_leq", Constraint(
                            expr=model.component(f"int_point_s{i}_c{k}_{j}_{q}_x") <= Tol + (b_1 - b_2)/(m_2 - m_1)))

                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_y_valid_leq", Constraint(
                            expr=model.component(f"int_point_s{i}_c{k}_{j}_{q}_y") <= Tol + m_1*(b_1 - b_2)/(m_2 - m_1) + b_1))

                        model.add_component(f"m1_s{i}_c{k}_{j}_{q}_valid_geq", Constraint(
                            expr=model.component(f"m1_s{i}_c{k}_{j}_{q}") + Tol >= (y_2 - y_1)/(x_2 - x_1)))

                        model.add_component(f"m2_s{i}_c{k}_{j}_{q}_valid_geq", Constraint(
                            expr=model.component(f"m1_s{i}_c{k}_{j}_{q}") + Tol >= (y_4 - y_3)/(x_4 - x_3)))

                        model.add_component(f"b1_s{i}_c{k}_{j}_{q}_valid_geq", Constraint(
                            expr=model.component(f"b1_s{i}_c{k}_{j}_{q}") + Tol >= -m_1*x_1 + y_1))

                        model.add_component(f"b2_s{i}_c{k}_{j}_{q}_valid_geq", Constraint(
                            expr=model.component(f"b2_s{i}_c{k}_{j}_{q}") + Tol >= -m_2*x_3 + y_3))

                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_x_valid_geq", Constraint(
                            expr=model.component(f"int_point_s{i}_c{k}_{j}_{q}_x") + Tol >= (b_1 - b_2)/(m_2 - m_1)))

                        model.add_component(f"int_point_s{i}_c{k}_{j}_{q}_y_valid_geq", Constraint(
                            expr=model.component(f"int_point_s{i}_c{k}_{j}_{q}_y") + Tol >= m_1*(b_1 - b_2)/(m_2 - m_1) + b_1))

    model.objective = Objective(expr=model.xyBound, sense=minimize)
    model.display()

    with open('test.txt', 'w') as sys.stdout:
        opt = SolverFactory('mindtpy')
        results = opt.solve(model, mip_solver='glpk',
                            nlp_solver='ipopt')
    if os.stat("test.txt").st_size == 0:
        is_feasible = True
    sys.stdout = sys.__stdout__

# model.objective.display()


win = GraphWin("My Squares", 1000, 1000)

for i in range(squares):
    scale = 1000/value(model.xyBound)
    print([Point(scale*value(model.component(f"c{j}_{i}_x")), scale*value(
        model.component(f"c{j}_{i}_y")))for j in range(4)])
    s = Polygon([Point(scale*value(model.component(f"c{j}_{i}_x")), scale*value(
        model.component(f"c{j}_{i}_y")))for j in range(4)])
    s.setFill("blue")
    s.draw(win)

win.getMouse()
