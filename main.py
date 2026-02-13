import numpy as np
from src import benchmark as bm
from src.fitness_fnc import sphere
#===========CONFIG================

T_MAX = 1000          # stop point
N_bats = 30         # population size
dim = 10             # dimension
bounds = (-5.0, 5.0) # bounds for each dimension
N_RUNS = 10         # number of benchmark runs

# Bat Algorithm hyperparameters
F_MIN = 0.0
F_MAX = 4.0
ALPHA = 0.95
GAMMA = 0.3

# Runtime options
SEED = 42
PLOT = True
VERBOSE = True
AUTO_GAMMA = False
USE_IMPROVED_LOCAL_WALK = False #require update_freq_velocity change from (bat.position - x_best) to (x_best - bat.position)

# ==========================================
if AUTO_GAMMA:
    if dim <= 5:
        GAMMA = 0.3
    elif 10 <= dim <= 30:
        GAMMA = 0.5
    else:
        GAMMA = 0.7
    print(f"Auto gamma set to: {GAMMA}")
# run benchmark

if __name__ == "__main__":
    print(f""" start benchmark...
          Objective function: Sphere Function
              dim: {dim}
              Bounds: [{bounds[0]}, {bounds[1]}]
          T_MAX: {T_MAX}
          N_RUNS: {N_RUNS}
          f_range: [{F_MIN}, {F_MAX}]
          alpha: {ALPHA}
          gamma: {GAMMA}
          improved_local_walk: {USE_IMPROVED_LOCAL_WALK}
          seed: {SEED}
          """)
    
    results = bm.benchmark_both_modes(
        objective_function=sphere,
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
        plot=PLOT,
        verbose=VERBOSE,
    )

    global_solution, global_fitness = results["global"]
    individual_solution, individual_fitness = results["individual"]

    print(f"[global] Best fitness found: {global_fitness:.6e}")
    print(f"[global] Best solution (first 5 dims): {global_solution[:5]}")
    print(f"[individual] Best fitness found: {individual_fitness:.6e}")
    print(f"[individual] Best solution (first 5 dims): {individual_solution[:5]}")
    