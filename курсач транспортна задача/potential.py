import numpy as np


def northwest_corner_method(cost, supply, demand):
    m, n = cost.shape
    x = np.zeros((m, n))
    i = j = 0

    while i < m and j < n:
        min_val = min(supply[i], demand[j])
        x[i, j] = min_val
        supply[i] -= min_val
        demand[j] -= min_val

        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1

    return x


def calculate_potentials(cost, x):
    m, n = cost.shape
    u = np.full(m, np.nan)
    v = np.full(n, np.nan)
    u[0] = 0

    while np.any(np.isnan(u)) or np.any(np.isnan(v)):
        for i in range(m):
            for j in range(n):
                if x[i, j] > 0:
                    if not np.isnan(u[i]) and np.isnan(v[j]):
                        v[j] = cost[i, j] - u[i]
                    elif np.isnan(u[i]) and not np.isnan(v[j]):
                        u[i] = cost[i, j] - v[j]
    return u, v


def find_entering_variable(cost, u, v):
    m, n = cost.shape
    delta = np.full((m, n), np.inf)
    for i in range(m):
        for j in range(n):
            if not np.isnan(u[i]) and not np.isnan(v[j]):
                delta[i, j] = cost[i, j] - (u[i] + v[j])
    min_val = np.min(delta)
    if min_val >= 0:
        return None
    return np.unravel_index(np.argmin(delta), delta.shape)


def find_loop(x, start):
    m, n = x.shape
    u, v = calculate_potentials(cost, x)
    delta = np.full((m, n), np.inf)
    for i in range(m):
        for j in range(n):
            if not np.isnan(u[i]) and not np.isnan(v[j]):
                delta[i, j] = cost[i, j] - (u[i] + v[j])

    for i in range(m):
        for j in range(n):
            if start[0] != i and start[1] != j:

                if delta[i, j] <= 0 and delta[start[0], j] == 0 and delta[i, start[1]] == 0:
                    loop = [(start[0], j), (i, j), (i, start[1]), (start[0], start[1])]
                    return loop
    return False


def adjust_solution(x, loop):
    if not loop:
        return
    loop_positions = loop[::2]
    loop_values = [x[i, j] for i, j in loop_positions]
    min_val = min(loop_values)

    for k, (i, j) in enumerate(loop):
        if k % 2 == 0:
            x[i, j] -= min_val
        else:
            x[i, j] += min_val


def optimize_transportation(cost, supply, demand):
    x = northwest_corner_method(cost, supply, demand)
    while True:
        u, v = calculate_potentials(cost, x)
        entering = find_entering_variable(cost, u, v)
        if entering is None:
            break
        loop = find_loop(x, entering)
        if not loop:
            break
        adjust_solution(x, loop)

    return x


cost = np.array([
    [8, 7, 5, 10],
    [13, 8, 10, 7],
    [12, 4, 11, 9]
])

supply = [240, 330, 180]
demand = [230, 220, 130, 170]

optimized_solution = optimize_transportation(cost, supply, demand)

print("Оптимізоване рішення:")
print(optimized_solution)
print("Загальна вартість транспортування:")
print(np.sum(optimized_solution * cost))
