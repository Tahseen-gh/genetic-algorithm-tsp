"""CLI entry point: run the GA and save the two plots from the notebook to disk."""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ga import run_ga, TOURNAMENT_SIZE


def plot_fitness_curve(best_distances, output_path):
    """Plot best tour distance per generation and save it to output_path."""
    plt.figure()
    plt.plot(range(1, len(best_distances) + 1), best_distances, marker='o')
    plt.xlabel("Generation")
    plt.ylabel("Best Tour Distance")
    plt.title("Best Tour Distance per Generation")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()


def plot_best_tour(best_tour, cities, output_path):
    """Visualize the best tour path and save it to output_path."""
    plt.figure()
    # make the tour a closed loop by appending the first city at the end
    best_path = best_tour + [best_tour[0]]
    x_coords = [cities[i][0] for i in best_path]
    y_coords = [cities[i][1] for i in best_path]
    plt.plot(x_coords, y_coords, marker='o')
    # coordinates for each city
    for idx, (x, y) in enumerate(cities):
        plt.text(x, y, str(idx))
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Best Tour Path")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genetic algorithm for the Traveling Salesman Problem."
    )
    parser.add_argument("--num-cities", type=int, default=10,
                         help="Number of cities to route between (default: 10)")
    parser.add_argument("--population-size", type=int, default=50,
                         help="Number of tours per generation (default: 50)")
    parser.add_argument("--generations", type=int, default=100,
                         help="Number of generations to run (default: 100)")
    parser.add_argument("--mutation-rate", type=float, default=0.2,
                         help="Probability of a swap mutation per child (default: 0.2)")
    parser.add_argument("--seed", type=int, default=None,
                         help="Random seed for reproducible runs (default: unseeded)")
    parser.add_argument("--output-dir", type=str, default="output",
                         help="Directory to save plots to (default: output)")
    args = parser.parse_args()

    if args.num_cities < 3:
        parser.error(
            f"--num-cities must be at least 3 (got {args.num_cities}); "
            "crossover picks two distinct crossover points from the city range, so below 3 cities it "
            "either has no valid pair to pick (and crashes) or only one possible pair, which just "
            "clones a parent instead of recombining two tours."
        )
    if args.population_size < TOURNAMENT_SIZE:
        parser.error(
            f"--population-size must be at least {TOURNAMENT_SIZE} (got {args.population_size}); "
            f"tournament selection samples {TOURNAMENT_SIZE} individuals without replacement each time it picks a parent."
        )

    return args


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    best_tour, best_distances, cities, converged = run_ga(
        num_cities=args.num_cities,
        pop_size=args.population_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        seed=args.seed,
    )

    fitness_curve_path = os.path.join(args.output_dir, "fitness_curve.png")
    best_tour_path = os.path.join(args.output_dir, "best_tour.png")
    plot_fitness_curve(best_distances, fitness_curve_path)
    plot_best_tour(best_tour, cities, best_tour_path)
    print(f"\nSaved plots to {fitness_curve_path} and {best_tour_path}")


if __name__ == "__main__":
    main()
