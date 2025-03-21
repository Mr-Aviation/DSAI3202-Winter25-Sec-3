# **Step 5.d: Running and Explaining the Algorithm**

## **Understanding `genetic_algorithm_trial.py`**

This script runs a **genetic algorithm** using functions from `genetic_algorithm.py`. Here’s how it works:

### **1. Load Distance Data**
```python
import pandas as pd
distance_matrix = pd.read_csv('./data/city_distances_cleaned.csv', header=None).to_numpy()
```
- Reads the distance data from `city_distances_cleaned.csv`.
- Converts it into a **NumPy array** for faster calculations.

### **2. Create Initial Population**
```python
population = generate_valid_population(distance_matrix, population_size=100, num_nodes=32)
```
- Generates **random routes** for the algorithm to work with.
- Each route **starts and ends** at the depot (node 0).
- Only **valid routes** (without invalid distances) are kept.

### **3. Run Genetic Algorithm**
```python
for generation in range(num_generations):
    fitness_scores = np.array([calculate_fitness(route, distance_matrix) for route in population])
    selected_parents = select_in_tournament(population, fitness_scores)
```
- Loops through a **fixed number of generations**.
- Calculates **fitness** for each route.
- Chooses the best routes (parents) for the next step.

### **4. Create New Routes**
```python
offspring = [mutate(order_crossover(selected_parents[i], selected_parents[i+1])) 
             for i in range(0, len(selected_parents), 2)]
```
- **Combines** routes from parents.
- **Mutates** some routes to introduce variation.

### **5. Replace Old Routes**
```python
population = offspring
```
- The **new routes** replace the old ones.
- The process continues until the algorithm stops.

### **6. Find the Best Route**
```python
best_idx = np.argmax(fitness_scores)
best_route = population[best_idx]
print(f"Best Route: {best_route}")
print(f"Total Distance: {fitness_scores[best_idx]}")
```
- Finds the **best route** in the final set.
- Prints the **total distance** of this route.

---

## **Output**
```
Best Solution: [24, 1, 5, 13, 4, 27, 0, 16, 9, 15, 18, 3, 2, 10, 8, 28, 17, 21, 31, 23, 12, 7, 30, 19, 29, 20, 14, 11, 22, 26, 6, 25]
Total Distance: -1000000.0
Time: 4.996480941772461 seconds
```

---

# **Step 6: Making the Algorithm Faster with MPI**

## **Which Parts Can Run in Parallel?**

### **1. Fitness Calculation**  
- Each route is evaluated **separately**.  
- **Why parallel?** Every fitness check is independent, so running them in parallel speeds things up.  

### **2. Parent Selection**  
- Tournaments to choose parents can happen **at the same time**.  
- **Why parallel?** Each selection doesn’t depend on the others.  

### **3. Creating New Routes**  
- Crossover and mutation happen on separate routes.  
- **Why parallel?** These steps don’t need to be in order.  

### **4. Creating a New Population**  
- If no progress is made, a fresh set of routes is created.  
- **Why parallel?** This can be done independently.  

---

---

## **Performance Improvement**

### **1. Speed Increase**
- Speedup = Old Time / New Time = **4.99 sec / 2.25 sec** = **2.2x faster**

### **2. Efficiency**
- Efficiency = Speedup / Number of Processes = **2.2 / 4** = **0.55**

---

## **How to Run the Parallel Code**
Run this command to use 4 processes:
```bash
mpirun -n 4 python3 parallel_genetic_algorithm.py
```