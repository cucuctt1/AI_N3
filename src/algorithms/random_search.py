import numpy as np


def _run_single_random_search(objective_function, dim, bounds, iterations, n_samples, seed=None):
    if seed is not None:
        np.random.seed(seed)

    lb, ub = bounds
    best_solution = np.random.uniform(lb, ub, dim)
    best_fitness = objective_function(best_solution)
    best_history = [best_fitness]

    for _ in range(iterations):
        candidates = np.random.uniform(lb, ub, (n_samples, dim))
        fitness_values = np.apply_along_axis(objective_function, 1, candidates)
        idx = int(np.argmin(fitness_values))

        if fitness_values[idx] < best_fitness:
            best_fitness = float(fitness_values[idx])
            best_solution = candidates[idx].copy()

        best_history.append(best_fitness)

    return best_solution, best_fitness, best_history


def benchmark_random_search(objective_function,
                            dim,
                            bounds,
                            iterations,
                            n_runs=30,
                            n_samples=30,
                            seed=None,
                            progress_callback=None,
                            verbose=True):
    run_solutions = []
    run_best_fitnesses = []
    run_histories = []

    for run_idx in range(n_runs):
        run_seed = None if seed is None else seed + run_idx
        best_solution, best_fitness, best_history = _run_single_random_search(
            objective_function=objective_function,
            dim=dim,
            bounds=bounds,
            iterations=iterations,
            n_samples=n_samples,
            seed=run_seed,
        )

        run_solutions.append(best_solution)
        run_best_fitnesses.append(best_fitness)
        run_histories.append(best_history)

        if verbose:
            print(f"[random_search] Run {run_idx + 1}/{n_runs} - Best Fitness: {best_fitness:.6e}")
        if progress_callback is not None:
            progress_callback("random_search", "single", run_idx + 1, n_runs)

    run_best_fitnesses = np.array(run_best_fitnesses, dtype=float)
    best_idx = int(np.argmin(run_best_fitnesses))

    return {
        "best_solution": run_solutions[best_idx],
        "best_fitness": float(run_best_fitnesses[best_idx]),
        "best_run_index": best_idx + 1,
        "mean_fitness": float(run_best_fitnesses.mean()),
        "std_fitness": float(run_best_fitnesses.std(ddof=0)),
        "run_best_fitnesses": run_best_fitnesses.tolist(),
        "best_history": run_histories[best_idx],
    }
