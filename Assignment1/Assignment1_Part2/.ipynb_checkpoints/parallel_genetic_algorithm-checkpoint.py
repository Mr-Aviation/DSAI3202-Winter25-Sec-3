from mpi4py import MPI
import numpy as np
import pandas as pd

def parallel_fitness(population, distance_matrix):
    """Compute fitness in parallel."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    chunk_size = len(population) // size
    local_population = population[rank * chunk_size:(rank + 1) * chunk_size]
    local_fitness = [calculate_fitness(route, distance_matrix) for route in local_population]
    
    all_fitness = comm.gather(local_fitness, root=0)
    if rank == 0:
        return np.concatenate(all_fitness)
    return None

def run_parallel_genetic_algorithm(distance_matrix, generations=100, pop_size=50):
    """Run the genetic algorithm in parallel."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    population = None
    if rank == 0:
        population = generate_population(pop_size, len(distance_matrix))
    
    population = comm.bcast(population, root=0)
    
    for _ in range(generations):
        fitness_scores = parallel_fitness(population, distance_matrix)
        if rank == 0:
            selected = select_in_tournament(population, fitness_scores)
            new_population = [mutate(order_crossover(*np.random.choice(selected, 2))) for _ in range(pop_size)]
        else:
            new_population = None
        
        population = comm.bcast(new_population, root=0)
    
    if rank == 0:
        best_idx = np.argmax(fitness_scores)
        return population[best_idx], -fitness_scores[best_idx]
    return None
