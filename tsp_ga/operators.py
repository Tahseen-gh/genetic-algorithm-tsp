"""GA operators: tournament selection, ordered crossover, swap mutation.

Ported as-is from the original notebook. ``tournament_selection`` now takes
``cities`` and ``tournament_size`` as parameters instead of reading them off
module globals; ``crossover`` and ``mutate`` are unchanged apart from
``mutation_rate`` becoming a parameter of ``mutate`` instead of a global.
"""
import random

from tour import fitness


def tournament_selection(population, cities, tournament_size):
    """Randomly select tournament_size individuals and return the best one."""
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda tour: fitness(tour, cities), reverse=True)
    return tournament[0]


def crossover(parent1, parent2):
    """Two-point order crossover (OX) with repair to keep the child a valid tour."""
    size = len(parent1)
    # two random crossover points i < j
    i, j = sorted(random.sample(range(size), 2))
    child = [None] * size
    # copy segment from parent1 into the child
    child[i:j+1] = parent1[i:j+1]
    # fill remaining positions with cities from parent2 in order
    pos = (j + 1) % size
    p2_index = (j + 1) % size
    while None in child:
        gene = parent2[p2_index]
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % size
        p2_index = (p2_index + 1) % size
    return child


def mutate(tour, mutation_rate):
    """Swap mutation: with probability mutation_rate, swap two cities in the tour."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour
