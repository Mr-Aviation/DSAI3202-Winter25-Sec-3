

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

population_size = 1000
spread_chance = 0.3
vaccination_rate = np.random.uniform(0.1, 0.5)

population = np.zeros(population_size)
np.random.seed(rank)

# Initial infection (only process 0)
if rank == 0:
    infected_indices = np.random.choice(population_size, int(0.1 * population_size), replace=False)
    population[infected_indices] = 1

def spread_virus(pop, chance, vac_rate):
    new_pop = pop.copy()
    for i in range(len(pop)):
        if pop[i] == 0 and np.random.rand() < chance * (1 - vac_rate):
            new_pop[i] = 1
    return new_pop

# Simulate virus spread
for _ in range(10):
    population = spread_virus(population, spread_chance, vaccination_rate)

# Gather results
if rank != 0:
    comm.send(population, dest=0, tag=rank)
else:
    total_population = population.copy()
    for i in range(1, size):
        recv_pop = comm.recv(source=i, tag=i)
        total_population += recv_pop

    total_infected = np.sum(total_population > 0)
    infection_rate = total_infected / (population_size * size)
    print(f"Final Infection Rate: {infection_rate:.4f}")

# Print individual infection rates
total_infected = np.sum(population > 0)
infection_rate = total_infected / population_size
print(f"Process {rank} Infection Rate: {infection_rate:.4f}")
