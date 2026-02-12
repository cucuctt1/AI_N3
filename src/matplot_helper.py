#matplotlib helper functions
#display plots using fitness data as 1D array
import matplotlib.pyplot as plt

def plot_fitness(fitness_history):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, marker='o', linestyle='-', color='b')
    plt.title('convergence curve')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.yscale('log')  # Log scale for better visibility
    plt.grid(True)
    plt.show()