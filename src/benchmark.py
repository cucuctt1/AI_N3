import numpy as np

from src.Bat import (
    evaluate_fitness,
    improved_local_random_walk_for_benchmark,
    initialize_population,
    local_random_walk_for_benchmark,
    selection_and_update_for_benchmark,
    update_freq_velocity,
    update_position,
)
from src.fitness_fnc import sphere
from src.matplot_helper import plot_fitness as default_plot_fitness


def _evaluate_population(population, objective_function):
    for bat in population:
        evaluate_fitness(bat, objective_function)
        if bat.fitness < bat.best_fitness:
            bat.best_fitness = bat.fitness
            bat.best_position = bat.position.copy()


def _run_single(objective_function, n_bats, dim, bounds, iterations,
                f_min, f_max, alpha, gamma, seed, behavior_mode,
                use_improved_local_walk=False):
    if seed is not None:
        np.random.seed(seed)

    population = initialize_population(n_bats, dim, bounds, f_min=f_min, f_max=f_max)
    _evaluate_population(population, objective_function)

    best_bat = min(population, key=lambda bat: bat.best_fitness)
    best_solution = best_bat.best_position.copy()
    best_fitness = best_bat.best_fitness
    fitness_history = [best_fitness]
    local_walk_fn = improved_local_random_walk_for_benchmark if use_improved_local_walk else local_random_walk_for_benchmark

    for iteration in range(1, iterations + 1):
        update_freq_velocity(population, best_solution, f_min=f_min, f_max=f_max)
        update_position(population, bounds)

        local_walk_fn(population, best_solution, bounds)
        best_solution, best_fitness = selection_and_update_for_benchmark(
            population,
            objective_function,
            best_solution,
            best_fitness,
            iteration,
            alpha=alpha,
            gamma=gamma,
            behavior_mode=behavior_mode,
        )
        fitness_history.append(best_fitness)

    return best_solution, best_fitness, fitness_history


def benchmark(objective_function=sphere,
              n_bats=30,
              dim=10,
              bounds=(-5.0, 5.0),
              iterations=1000,
              n_runs=10,
              f_min=0.0,
              f_max=2.0,
              alpha=0.9,
              gamma=0.9,
              use_improved_local_walk=False,
              behavior_mode="individual",
              seed=None,
              plot=True,
              verbose=True,
              return_best_history=False):
    run_results = []

    for run_idx in range(n_runs):
        run_seed = None if seed is None else seed + run_idx
        best_solution, best_fitness, fitness_history = _run_single(
            objective_function=objective_function,
            n_bats=n_bats,
            dim=dim,
            bounds=bounds,
            iterations=iterations,
            f_min=f_min,
            f_max=f_max,
            alpha=alpha,
            gamma=gamma,
            seed=run_seed,
            behavior_mode=behavior_mode,
            use_improved_local_walk=use_improved_local_walk,
        )
        run_results.append((best_solution, best_fitness, fitness_history))

        if verbose:
            print(f"[{behavior_mode}] Run {run_idx + 1}/{n_runs} - Best Fitness: {best_fitness:.6e}")

    best_idx = int(np.argmin([result[1] for result in run_results]))
    best_solution, best_fitness, best_history = run_results[best_idx]
    all_fitness = np.array([result[1] for result in run_results], dtype=float)

    if verbose:
        print("=" * 60)
        print(f"Benchmark ({behavior_mode}) finished over {n_runs} runs")
        print(f"Best run index : {best_idx + 1}")
        print(f"Best fitness   : {best_fitness:.6e}")
        print(f"Mean fitness   : {all_fitness.mean():.6e}")
        print(f"Std fitness    : {all_fitness.std(ddof=0):.6e}")
        print("=" * 60)

    if plot:
        default_plot_fitness({behavior_mode: best_history})

    if return_best_history:
        return best_solution, best_fitness, best_history

    return best_solution, best_fitness


def benchmark_both_modes(objective_function=sphere,
                         n_bats=30,
                         dim=10,
                         bounds=(-5.0, 5.0),
                         iterations=1000,
                         n_runs=10,
                         f_min=0.0,
                         f_max=2.0,
                         alpha=0.9,
                         gamma=0.9,
                         use_improved_local_walk=False,
                         seed=None,
                         plot=True,
                         verbose=True):
    mode_results = {}
    mode_histories = {}

    for mode in ["global", "individual"]:
        mode_seed = seed if seed is None else seed + (0 if mode == "global" else 10000)
        best_solution, best_fitness, best_history = benchmark(
            objective_function=objective_function,
            n_bats=n_bats,
            dim=dim,
            bounds=bounds,
            iterations=iterations,
            n_runs=n_runs,
            f_min=f_min,
            f_max=f_max,
            alpha=alpha,
            gamma=gamma,
            use_improved_local_walk=use_improved_local_walk,
            behavior_mode=mode,
            seed=mode_seed,
            plot=False,
            verbose=verbose,
            return_best_history=True,
        )
        mode_results[mode] = (best_solution, best_fitness)
        mode_histories[mode] = best_history

    if verbose:
        print("=" * 60)
        print("Mode comparison summary")
        print(f"Global best fitness    : {mode_results['global'][1]:.6e}")
        print(f"Individual best fitness: {mode_results['individual'][1]:.6e}")
        print("=" * 60)

    if plot:
        default_plot_fitness(mode_histories)

    return mode_results