import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value


def solve_transportation_problem(cost, supply, demand):
    m, n = cost.shape
    prob = LpProblem("Transportation_Problem", LpMinimize)

    # Define decision variables
    x = [[LpVariable(f'x_{i}_{j}', lowBound=0, cat='Continuous') for j in range(n)] for i in range(m)]

    # Objective function
    prob += lpSum(cost[i][j] * x[i][j] for i in range(m) for j in range(n))

    # Supply constraints
    for i in range(m):
        prob += lpSum(x[i][j] for j in range(n)) == supply[i]

    # Demand constraints
    for j in range(n):
        prob += lpSum(x[i][j] for i in range(m)) == demand[j]

    # Solve the problem
    prob.solve()

    # Extract the solution
    solution = np.array([[value(x[i][j]) for j in range(n)] for i in range(m)])

    return solution, value(prob.objective)


# Example usage
cost = np.array([
    [8, 7, 5, 10],
    [13, 8, 10, 7],
    [12, 4, 11, 9]
])

supply = [240, 330, 180]
demand = [230, 220, 130, 170]

optimized_solution, objective_value = solve_transportation_problem(cost, supply, demand)
print("Optimized solution using PuLP:")
print(optimized_solution)
print("Objective function value (total transportation cost):")
print(objective_value)
