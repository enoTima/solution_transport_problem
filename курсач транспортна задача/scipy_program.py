import numpy as np
from scipy.optimize import linprog


def solve_transportation_problem_scipy(cost, supply, demand):
    m, n = cost.shape
    c = cost.flatten()

    # Create equality constraints for supply
    A_eq = np.zeros((m + n, m * n))
    b_eq = np.concatenate((supply, demand))

    for i in range(m):
        for j in range(n):
            A_eq[i, i * n + j] = 1

    # Create equality constraints for demand
    for j in range(n):
        for i in range(m):
            A_eq[m + j, i * n + j] = 1

    bounds = [(0, None) for _ in range(m * n)]

    # Solve the linear programming problem
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        solution = result.x.reshape(m, n)
        return solution, result.fun
    else:
        raise ValueError("Linear programming did not converge")


# Example usage
cost = np.array([
    [8, 7, 5, 10],
    [13, 8, 10, 7],
    [12, 4, 11, 9]
])

supply = [240, 330, 180]
demand = [230, 220, 130, 170]

optimized_solution, objective_value = solve_transportation_problem_scipy(cost, supply, demand)
print("Optimized solution using SciPy:")
print(optimized_solution)
print("Total transportation cost:")
print(objective_value)
