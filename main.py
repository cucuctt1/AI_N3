import numpy as np
from src import benchmark as bm
from src.fitness_fnc import sphere
#===========CONFIG================

T_MAX = 200          # stop point
N_bats = 30         # population size
dim = 10             # dimension
bounds = (-5.0, 5.0) # bounds for each dimension


# ==========================================

# run benchmark

if __name__ == "__main__":
    print(f""" start benchmark...
          Objective function: Sphere Function
              dim: {dim}
              Bounds: [{bounds[0]}, {bounds[1]}]
          T_MAX: {T_MAX}
          """)
    
    results = bm.benchmark_both_modes(
        objective_function=sphere,
        n_bats=N_bats,
        dim=dim,
        bounds=bounds,
        iterations=T_MAX,
        n_runs=10,
        seed=42,
        plot=True,
        verbose=True,
    )

    global_solution, global_fitness = results["global"]
    individual_solution, individual_fitness = results["individual"]

    print(f"[global] Best fitness found: {global_fitness:.6e}")
    print(f"[global] Best solution (first 5 dims): {global_solution[:5]}")
    print(f"[individual] Best fitness found: {individual_fitness:.6e}")
    print(f"[individual] Best solution (first 5 dims): {individual_solution[:5]}")
    