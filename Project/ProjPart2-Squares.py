from pyomo.opt import SolverFactory

from pyomo.opt import SolverStatus, TerminationCondition

import pyomo
import random

from pyomo.environ import *
from graphics import *

squares = 2

is_feasible = False

while (not is_feasible):
    model = ConcreteModel("Squares")

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

    model.objective = Objective(expr=model.xyBound, sense=minimize)

    # opt = SolverFactory('couenne')
    # opt.solve(model)

    opt = SolverFactory('mindtpy')
    results = opt.solve(model, mip_solver='glpk',
                        nlp_solver='ipopt')
    if ((not results.solver.termination_condition == TerminationCondition.infeasible)):
        is_feasible = True

# model.objective.display()
# model.display()

# win = GraphWin("My Squares", 1000, 1000)

# for i in range(squares):
#     scale = 1000/value(model.xyBound)
#     print([Point(scale*value(model.component(f"c{j}_{i}_x")), scale*value(
#         model.component(f"c{j}_{i}_y")))for j in range(4)])
#     s = Polygon([Point(scale*value(model.component(f"c{j}_{i}_x")), scale*value(
#         model.component(f"c{j}_{i}_y")))for j in range(4)])
#     s.setFill("blue")
#     s.draw(win)

# win.getMouse()
