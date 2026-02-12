import numpy as np

class Bat_obj:
    #object initialize
    def __init__(self, dim, bounds, f_min=0.0, f_max=2.0, A_init=1.0, r_init=0.1):
        lb, ub = bounds
        self.position = np.random.uniform(lb, ub, dim)
        self.velocity = np.zeros(dim)
        self.frequency = np.random.uniform(0.0, 2.0)
        self.loudness = 1.0
        self.pulse_rate = 0.1
        self.r_init = 0.1
        self.best_position = self.position.copy()
        self.best_fitness = float("inf")
    
    def __str__(self):
        return f"Tham số dơi: position={self.position}, velocity={self.velocity}, frequency={self.frequency}, loudness={self.loudness}, pulse_rate={self.pulse_rate}"

# bat function
    
def initialize_population(n_bats, dim, bounds, f_min=0.0, f_max=2.0, 
                          A_init=1.0, r_init=0.1) -> list:
    #init bat population
    population = []
    for i in range(n_bats):
        bat = Bat_obj(dim, bounds, f_min, f_max, A_init, r_init)
        population.append(bat)
    return population

def update_freq_velocity(population, x_best, f_min=0.0, f_max=2.0) -> None:
    # update frequency and velocity
    for bat in population:
        beta = np.random.uniform(0, 1)
        bat.frequency = f_min + (f_max - f_min) * beta
        bat.velocity = bat.velocity + (bat.position - x_best) * bat.frequency

def evaluate_fitness(bat, target_function) -> None:
    # evaluate fitness
    bat.fitness = target_function(bat.position)


def evealuate_fitness(bat, target_function) -> None:
    evaluate_fitness(bat, target_function)


def update_position(population, bounds) -> None:
    lb, ub = bounds
    for bat in population:
        bat.position = np.clip(bat.position + bat.velocity, lb, ub)

def update_behavior(population, iteration, alpha=0.9, gamma=0.9, mode="global"):
    """Cập nhật hành vi dơi (A và r)"""
    if mode == "global":
        # global mode: all bats use same A and r
        avg_loudness = np.mean([bat.loudness for bat in population])
        avg_pulse_rate = np.mean([bat.pulse_rate for bat in population]) #unsused
        
        new_loudness = avg_loudness * alpha
        new_pulse_rate = population[0].r_init * (1 - np.exp(-gamma * iteration))
        
        for bat in population:
            bat.loudness = new_loudness
            bat.pulse_rate = new_pulse_rate
    
    elif mode == "individual":
        # individual mode: update A and r for each bat
        for bat in population:
            bat.loudness *= alpha
            bat.pulse_rate = bat.r_init * (1 - np.exp(-gamma * iteration))


    

