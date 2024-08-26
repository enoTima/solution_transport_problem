from ortools.linear_solver import pywraplp
import numpy as np


def solve_transportation_problem_ortools(cost, supply, demand):
    m, n = cost.shape
    solver = pywraplp.Solver.CreateSolver('GLOP')

    x = {}
    for i in range(m):
        for j in range(n):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')

    # Supply constraints
    for i in range(m):
        solver.Add(solver.Sum(x[i, j] for j in range(n)) == supply[i])

    # Demand constraints
    for j in range(n):
        solver.Add(solver.Sum(x[i, j] for i in range(m)) == demand[j])

    # Objective function
    objective = solver.Sum(cost[i, j] * x[i, j] for i in range(m) for j in range(n))
    solver.Minimize(objective)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = np.array([[x[i, j].solution_value() for j in range(n)] for i in range(m)])
        return solution, solver.Objective().Value()
    else:
        raise ValueError("The problem does not have an optimal solution.")


# Example usage
cost = np.array([
    [8, 7, 5, 10],
    [13, 8, 10, 7],
    [12, 4, 11, 9]
])

supply = [240, 330, 180]
demand = [230, 220, 130, 170]

optimized_solution, objective_value = solve_transportation_problem_ortools(cost, supply, demand)
print("Optimized solution using OR-Tools:")
print(optimized_solution)
print("Objective function value (total transportation cost):")
print(objective_value)
