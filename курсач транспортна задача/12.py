import numpy as np
import time

def northwest_corner_method(cost, supply, demand):
    m, n = cost.shape
    x = np.zeros((m, n))
    i = j = 0

    while i < m and j < n:
        min_val = min(supply[i], demand[j])
        x[i, j] = min_val
        supply[i] -= min_val
        demand[j] -= min_val

        if supply[i] == 0 and i < m - 1:
            i += 1
        elif demand[j] == 0 and j < n - 1:
            j += 1
        elif supply[i] == 0 and i == m - 1:
            j += 1
        elif demand[j] == 0 and j == n - 1:
            i += 1

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
                    print(u)
                    print(v)
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
    visited = set()
    def dfs(i, j, parent, path):
        if (i, j) in visited:
            if (i, j) == start:
                return path
            return None
        visited.add((i, j))
        if parent and path and (i, j) == start:
            return path
        # Explore horizontally and vertically
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and (ni, nj) != parent and (x[ni, nj] > 0 or (ni, nj) == start):
                result = dfs(ni, nj, (i, j), path + [(ni, nj)])
                if result:
                    return result
        visited.remove((i, j))
        return None

    return dfs(start[0], start[1], None, [start])

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
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply > total_demand:
        # Add a dummy demand column
        cost = np.column_stack((cost, np.zeros(cost.shape[0])))
        demand = np.append(demand, total_supply - total_demand)
    elif total_demand > total_supply:
        # Add a dummy supply row
        cost = np.row_stack((cost, np.zeros(cost.shape[1])))
        supply = np.append(supply, total_demand - total_supply)
    print(demand)
    print(supply)

    x = northwest_corner_method(cost, supply, demand)
    while True:
        u, v = calculate_potentials(cost, x)
        print(u, v)
        entering = find_entering_variable(cost, u, v)
        if entering is None:
            break
        loop = find_loop(x, entering)
        if not loop:
            break
        adjust_solution(x, loop)

    return x


def generate_random_transportation_problem():
    max_supply = 30
    max_demand = 30
    max_cost = 20
    num_sources = np.random.randint(2, 100)
    num_destinations = np.random.randint(2, 100)
    cost = np.random.randint(1, max_cost + 1, size=(num_sources, num_destinations))
    supply = np.random.randint(1, max_supply + 1, size=num_sources)
    demand = np.random.randint(1, max_demand + 1, size=num_destinations)
    total_supply = np.sum(supply)
    total_demand = np.sum(demand)
    if total_supply > total_demand:
        extra_demand = total_supply - total_demand
        demand = np.append(demand, extra_demand)
        cost = np.hstack((cost, np.random.randint(1, max_cost + 1, size=(num_sources, 1))))
    elif total_demand > total_supply:
        extra_supply = total_demand - total_supply
        supply = np.append(supply, extra_supply)
        cost = np.vstack((cost, np.random.randint(1, max_cost + 1, size=(1, num_destinations))))
    return cost, supply, demand




time4 = []
for i in range(10):
    np.set_printoptions(threshold=np.inf)
    print(i)
    cost, supply, demand = generate_random_transportation_problem()

    tic4 = time.time()
    optimize_transportation(cost, supply, demand)
    toc4 = time.time()
    time4.append(toc4 - tic4)

print(f'середній час виконання власної програми: {np.mean(time4):.8f}')
