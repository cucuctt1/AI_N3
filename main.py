import numpy as np
from datetime import datetime
from pathlib import Path

from src import benchmark as bm
from src.algorithms.random_search import benchmark_random_search
from src.fitness_fnc import sphere, rastrigin, rosenbrock, ackley, griewank
from src.matplot_helper import plot_fitness
from src.utils.io_utils import save_benchmark_stats_csv
#===========CONFIG================

T_MAX = 1000          # stop point
N_bats = 30         # population size
dim = 10             # dimension
bounds = (-5.0, 5.0) # bounds for each dimension
N_RUNS = 30         # number of benchmark runs

# Bat Algorithm hyperparameters
F_MIN = 0.0
F_MAX = 4.0
ALPHA = 0.95
GAMMA = 0.3

# Runtime options
SEED = 42
PLOT = True
PLOT_SHOW_MODE = "last"  # none | all | last
VERBOSE = True
AUTO_GAMMA = False
USE_IMPROVED_LOCAL_WALK = False #require update_freq_velocity change from (bat.position - x_best) to (x_best - bat.position)
TRACK_PROGRESS = True

# ==========================================
if AUTO_GAMMA:
    if dim <= 5:
        GAMMA = 0.3
    elif 10 <= dim <= 30:
        GAMMA = 0.5
    else:
        GAMMA = 0.7
    print(f"Auto gamma set to: {GAMMA}")

BENCHMARK_FUNCTIONS = {
    "sphere": sphere,
    "rastrigin": rastrigin,
    "rosenbrock": rosenbrock,
    "ackley": ackley,
    "griewank": griewank,
}
def _print_table(rows):
    print("\n" + "=" * 92)
    print(f"{'Objective':<12} {'Algorithm':<16} {'Best':>14} {'Mean':>14} {'Std':>14} {'BestRun':>10}")
    print("-" * 92)
    for row in rows:
        print(
            f"{row['objective']:<12} "
            f"{row['algorithm']:<16} "
            f"{row['best_fitness']:>14.6e} "
            f"{row['mean_fitness']:>14.6e} "
            f"{row['std_fitness']:>14.6e} "
            f"{int(row['best_run_index']):>10}"
        )
    print("=" * 92)
# run benchmark

if __name__ == "__main__":
    print(f""" start benchmark suite...
          Objectives: {', '.join(BENCHMARK_FUNCTIONS.keys())}
          dim: {dim}
          Bounds: [{bounds[0]}, {bounds[1]}]
          T_MAX: {T_MAX}
          N_RUNS (BA mỗi benchmark): {N_RUNS}
          f_range: [{F_MIN}, {F_MAX}]
          alpha: {ALPHA}
          gamma: {GAMMA}
          improved_local_walk: {USE_IMPROVED_LOCAL_WALK}
          seed: {SEED}
          """)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("images") / "runs" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    table_rows = []
    total_progress_steps = len(BENCHMARK_FUNCTIONS) * N_RUNS * 3
    progress_state = {"done": 0}

    def _progress_callback(algorithm, mode, run_idx, total_runs):
        if not TRACK_PROGRESS:
            return
        progress_state["done"] += 1
        pct = (progress_state["done"] / total_progress_steps) * 100.0
        print(
            f"[progress] {progress_state['done']}/{total_progress_steps} ({pct:6.2f}%) "
            f"{algorithm}:{mode} run {run_idx}/{total_runs}"
        )

    objective_names = list(BENCHMARK_FUNCTIONS.keys())
    for obj_idx, (objective_name, objective_fn) in enumerate(BENCHMARK_FUNCTIONS.items()):
        if VERBOSE:
            print(f"\n>>> Benchmark objective: {objective_name}")

        ba_results = bm.benchmark_both_modes(
            objective_function=objective_fn,
            n_bats=N_bats,
            dim=dim,
            bounds=bounds,
            iterations=T_MAX,
            n_runs=N_RUNS,
            f_min=F_MIN,
            f_max=F_MAX,
            alpha=ALPHA,
            gamma=GAMMA,
            use_improved_local_walk=USE_IMPROVED_LOCAL_WALK,
            seed=SEED,
            progress_callback=_progress_callback,
            plot=False,
            verbose=VERBOSE,
            return_details=True,
        )

        random_results = benchmark_random_search(
            objective_function=objective_fn,
            dim=dim,
            bounds=bounds,
            iterations=T_MAX,
            n_runs=N_RUNS,
            n_samples=N_bats,
            seed=SEED,
            progress_callback=_progress_callback,
            verbose=VERBOSE,
        )

        bat_only_curves = {
            "ba_global": ba_results["global"]["best_history"],
            "ba_individual": ba_results["individual"]["best_history"],
        }

        all_compare_curves = {
            "ba_global": ba_results["global"]["best_history"],
            "ba_individual": ba_results["individual"]["best_history"],
            "random_search": random_results["best_history"],
        }

        show_now = (
            PLOT and (
                PLOT_SHOW_MODE == "all"
                or (PLOT_SHOW_MODE == "last" and obj_idx == len(objective_names) - 1)
            )
        )

        plot_fitness(
            bat_only_curves,
            title=f"{objective_name} - BA only",
            save_path=str(output_dir / f"{objective_name}_bat_only.png"),
            show=show_now,
        )

        plot_fitness(
            all_compare_curves,
            title=f"{objective_name} - BA vs Random Search",
            save_path=str(output_dir / f"{objective_name}_comparison.png"),
            show=show_now,
        )

        table_rows.extend([
            {
                "objective": objective_name,
                "algorithm": "ba_global",
                "best_fitness": ba_results["global"]["best_fitness"],
                "mean_fitness": ba_results["global"]["mean_fitness"],
                "std_fitness": ba_results["global"]["std_fitness"],
                "best_run_index": ba_results["global"]["best_run_index"],
            },
            {
                "objective": objective_name,
                "algorithm": "ba_individual",
                "best_fitness": ba_results["individual"]["best_fitness"],
                "mean_fitness": ba_results["individual"]["mean_fitness"],
                "std_fitness": ba_results["individual"]["std_fitness"],
                "best_run_index": ba_results["individual"]["best_run_index"],
            },
            {
                "objective": objective_name,
                "algorithm": "random_search",
                "best_fitness": random_results["best_fitness"],
                "mean_fitness": random_results["mean_fitness"],
                "std_fitness": random_results["std_fitness"],
                "best_run_index": random_results["best_run_index"],
            },
        ])

    csv_path = save_benchmark_stats_csv(table_rows, output_dir)
    _print_table(table_rows)

    print(f"\nSaved outputs in: {output_dir}")
    print(f"- Stats CSV: {csv_path}")
    print("- Curves: one BA-only and one full-comparison image per objective")
    