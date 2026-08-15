"""Tour representation: city generation, distance, and fitness.

A tour is a list of city indices (a permutation of range(num_cities)).
Ported as-is from the original notebook; only the module-level globals
(``cities``, ``NUM_CITIES``) became explicit function parameters so this
can be imported from other files instead of relying on notebook globals.
"""
import random
import math


def generate_cities(num_cities):
    """Generate random x, y coordinates in the range [0, 100] for each city."""
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]


def euclidean_distance(city1, city2):
    """Compute Euclidean distance between two cities."""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)


def total_distance(tour, cities):
    """Compute the total distance of a tour, including return to the starting city."""
    distance = 0
    for i in range(len(tour)):
        city_a = cities[tour[i]]
        city_b = cities[tour[(i+1) % len(tour)]]
        distance += euclidean_distance(city_a, city_b)
    return distance


def generate_random_tour(num_cities):
    """Generate a random permutation of city indices."""
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour


def fitness(tour, cities):
    """Fitness is the inverse of tour distance, so shorter tours score higher."""
    d = total_distance(tour, cities)
    return 1.0 / d if d != 0 else float('inf')
