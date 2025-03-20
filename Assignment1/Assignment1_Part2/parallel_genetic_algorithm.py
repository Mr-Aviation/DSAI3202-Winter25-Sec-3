from mpi4py import MPI
import time
import pandas as pd
import numpy as np
from genetic_algorithm import generate_population, mutate, calculate_fitness, select_in_tournament, order_crossover

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Start timing
start_time = time.time()

# Load distance matrix (only once on rank 0, then broadcast)
if rank == 0:
    distance_matrix = pd.read_csv('Assignment1/Assignment1_Part2/data/city_distances_cleaned.csv').to_numpy()
else:
    distance_matrix = None

distance_matrix = comm.bcast(distance_matrix, root=0)

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 10000
mutation_rate = 0.1
num_generations = 200
stagnation_limit = 5

# Generate initial population (only on rank 0)
if rank == 0:
    population = generate_population(population_size, num_nodes)
else:
    population = None

# Broadcast population to all ranks
population = comm.bcast(population, root=0)

# Scatter population across processes
local_population_size = population_size // size
local_population = comm.scatter([population[i:i+local_population_size] for i in range(0, population_size, local_population_size)], root=0)

# Function for local fitness computation
def evaluate_fitness(local_population):
    return np.array([calculate_fitness(route, distance_matrix) for route in local_population])

# Main GA loop
for generation in range(num_generations):
    # Compute local fitness values
    local_fitness_values = evaluate_fitness(local_population)

    # Gather fitness values from all processes
    global_fitness_values = comm.gather(local_fitness_values, root=0)

    if rank == 0:
        global_fitness_values = np.concatenate(global_fitness_values)

        # Selection
        selected = select_in_tournament(population, global_fitness_values)

        # Perform crossover and mutation
        offspring = [order_crossover(selected[i], selected[i+1]) for i in range(0, len(selected), 2)]
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replace worst individuals
        worst_indices = np.argsort(global_fitness_values)[-len(mutated_offspring):]
        for i, idx in enumerate(worst_indices):
            population[idx] = mutated_offspring[i]

    # Scatter new population across processes
    local_population = comm.scatter([population[i:i+local_population_size] for i in range(0, population_size, local_population_size)], root=0)

    if rank == 0:
        print(f"Generation {generation}: Best fitness = {np.min(global_fitness_values)}")

# Final gathering of the population
final_population = comm.gather(local_population, root=0)

# Stop timing
end_time = time.time()

# Output best solution and execution time
if rank == 0:
    # Flatten final_population to avoid inhomogeneous structure
    final_population = [item for sublist in final_population for item in sublist]  # Flatten the list
    final_fitness_values = evaluate_fitness(final_population)
    best_idx = np.argmin(final_fitness_values)
    best_solution = final_population[best_idx]
    print("Best Solution:", best_solution)
    print("Total Distance:", final_fitness_values[best_idx])
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
