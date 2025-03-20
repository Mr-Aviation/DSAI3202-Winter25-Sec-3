import numpy as np
import pandas as pd

def calculate_fitness(route, distance_matrix):
    """Calculate total distance of a given route."""
    total_distance = 0
    for i in range(len(route) - 1):
        dist = distance_matrix[route[i], route[i + 1]]
        if dist == 100000:
            return -1e6  # Penalize invalid routes
        total_distance += dist
    total_distance += distance_matrix[route[-1], route[0]]  # Return to depot
    return -total_distance  # Minimize distance

def select_in_tournament(population, scores, num_tournaments=4, tournament_size=3):
    """Tournament selection for genetic algorithm."""
    selected = []
    for _ in range(num_tournaments):
        idx = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = idx[np.argmax(scores[idx])]
        selected.append(population[best_idx])
    return selected

def order_crossover(parent1, parent2):
    """Perform ordered crossover between two parents."""
    size = len(parent1)
    start, end = sorted(np.random.choice(range(size), 2, replace=False))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    p2_values = [x for x in parent2 if x not in child]
    child = [p2_values.pop(0) if x == -1 else x for x in child]
    return child

def mutate(route, mutation_rate=0.1):
    """Swap mutation with a given probability."""
    if np.random.rand() < mutation_rate:
        idx1, idx2 = np.random.choice(len(route), 2, replace=False)
        route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

def generate_population(size, num_nodes):
    """Generate an initial population of random routes."""
    return [np.random.permutation(num_nodes).tolist() for _ in range(size)]
