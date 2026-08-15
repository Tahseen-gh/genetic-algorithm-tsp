"""Main GA loop for the Traveling Salesman Problem.

The loop body is the same sequence of steps as the original notebook
(evaluate + sort, track the best, print progress, keep the elites, breed
the rest, check convergence). It's now wrapped in ``run_ga`` and reads
population size / generations / mutation rate / city count from arguments
instead of module-level constants, so it can be driven from the CLI.
Tournament size and elite count were not in the notebook's set of
"things you configure per run" outside editing the constants, so they
stay as module constants here, at their original values.
"""
import random

from tour import generate_cities, generate_random_tour, total_distance, fitness
from operators import tournament_selection, crossover, mutate

TOURNAMENT_SIZE = 3
ELITE_COUNT = 2

# Convergence is declared when the best distance barely moves over this many
# generations. 20 and 1e-6 are the thresholds from the original notebook.
CONVERGENCE_WINDOW = 20
CONVERGENCE_THRESHOLD = 1e-6


def initial_population(pop_size, num_cities):
    """Generate an initial population of random tours."""
    return [generate_random_tour(num_cities) for _ in range(pop_size)]


def run_ga(num_cities, pop_size, generations, mutation_rate, seed=None):
    """Run the genetic algorithm.

    Returns (best_tour, best_distances, cities, converged), where
    best_distances[g] is the best tour distance found in generation g + 1.
    """
    if seed is not None:
        random.seed(seed)

    cities = generate_cities(num_cities)

    population = initial_population(pop_size, num_cities)
    best_distances = []
    best_tour = None
    best_fitness = 0

    for generation in range(generations):
        # Evaluate fitness for the current population and sort putting best at first
        population = sorted(population, key=lambda t: fitness(t, cities), reverse=True)
        current_best = population[0]
        current_best_fitness = fitness(current_best, cities)
        best_distances.append(total_distance(current_best, cities))

        # Update global best if improvement is found
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_tour = current_best[:]

        print(f"Generation {generation + 1}: Best Distance = {total_distance(current_best, cities):.2f}")

        # retain the top ELITE_COUNT individuals
        new_population = population[:ELITE_COUNT]

        # Create offspring until the new population is complete
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, cities, TOURNAMENT_SIZE)
            parent2 = tournament_selection(population, cities, TOURNAMENT_SIZE)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    final_distance = total_distance(best_tour, cities)
    print("\nFinal best tour distance:", final_distance)

    # if the best distance in the last 20 generations changes in a negligible manner, consider it converged
    window = best_distances[-CONVERGENCE_WINDOW:]
    converged = max(window) - min(window) < CONVERGENCE_THRESHOLD
    if converged:
        print("The algorithm has converged.")
    else:
        print("The algorithm has not fully converged.")

    return best_tour, best_distances, cities, converged
