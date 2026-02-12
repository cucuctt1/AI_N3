#matplotlib helper functions
#display plots using fitness data as 1D array
import matplotlib.pyplot as plt

def plot_fitness(fitness_history):
    if isinstance(fitness_history, dict):
        curves = fitness_history
    else:
        curves = {"fitness": fitness_history}

    plt.figure(figsize=(10, 6))
    for label, history in curves.items():
        plt.plot(history, linestyle='-', label=label)

    plt.title('convergence curve')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.yscale('log')  # Log scale for better visibility
    plt.grid(True)
    if len(curves) > 1:
        plt.legend()
    plt.show()