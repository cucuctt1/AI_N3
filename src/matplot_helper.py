#matplotlib helper functions
#display plots using fitness data as 1D array
import matplotlib.pyplot as plt
import numpy as np

def plot_fitness(fitness_history, title='convergence curve', save_path=None, show=True):
    if isinstance(fitness_history, dict):
        curves = fitness_history
    else:
        curves = {"fitness": fitness_history}

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))
    for label, history in curves.items():
        y = np.maximum(np.asarray(history, dtype=float), 1e-12)
        marker_step = max(len(y) // 12, 1)
        plt.plot(y, linestyle='-', marker='o', markevery=marker_step, linewidth=1.8, label=label)

    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.yscale('log')  # Log scale for better visibility
    plt.grid(True)
    if len(curves) > 1:
        plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()