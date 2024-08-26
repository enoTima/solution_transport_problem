import time
import numpy as np
from pulpprogram import solve_transportation_problem
from scipy_program import solve_transportation_problem_scipy
from ortools_program import solve_transportation_problem_ortools


def generate_random_transportation_problem():
    max_supply = 300
    max_demand = 300
    max_cost = 20
    num_sources = np.random.randint(100)
    num_destinations = np.random.randint(100)
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


time1 = []
time2 = []
time3 = []
for i in range(100):
    cost, supply, demand = generate_random_transportation_problem()


    tic1 = time.time()
    solve_transportation_problem(cost, supply, demand)
    toc1 = time.time()
    time1.append(toc1 - tic1)

    tic2 = time.time()
    solve_transportation_problem_ortools(cost, supply, demand)
    toc2 = time.time()
    time2.append(toc2 - tic2)

    tic3 = time.time()
    solve_transportation_problem_scipy(cost, supply, demand)
    toc3 = time.time()
    time3.append(toc3 - tic3)

print(f'середній час виконання pulp: {np.mean(time1):.8f}')
print(f'середній час виконання ortools: {np.mean(time2):.8f}')
print(f'середній час виконання scipy: {np.mean(time3):.8f}')
