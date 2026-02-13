import numpy as np

class Bat_obj:
    #object initialize
    def __init__(self, dim, bounds, f_min=0.0, f_max=2.0, A_init=1.0, r_init=0.1):
        lb, ub = bounds
        self.position = np.random.uniform(lb, ub, dim)
        self.velocity = np.zeros(dim)
        self.frequency = np.random.uniform(f_min, f_max)
        self.loudness = A_init
        self.pulse_rate = r_init
        self.r_init = r_init
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
            # bat.loudness *= alpha ////remove duplicate update in selection_and_update 
            bat.pulse_rate = bat.r_init * (1 - np.exp(-gamma * iteration))

def update_position_reflect(population, bounds):
    """Cập nhật vị trí nâng cao: Cơ chế bật tường (Reflect) - Vector hóa."""
    lb, ub = bounds
    for bat in population:
        new_pos = bat.position + bat.velocity
       
        # Xử lý vượt cận trên (Upper bound)
        over_ub = new_pos > ub
        new_pos[over_ub] = 2 * ub - new_pos[over_ub]
        bat.velocity[over_ub] *= -1  # Đảo chiều vận tốc

        # Xử lý vượt cận dưới (Lower bound)
        under_lb = new_pos < lb
        new_pos[under_lb] = 2 * lb - new_pos[under_lb]
        bat.velocity[under_lb] *= -1 # Đảo chiều vận tốc

        # Đảm bảo an toàn tuyệt đối
        bat.position = np.clip(new_pos, lb, ub)

def local_random_walk(population, x_best, bounds):
    lb, ub = bounds
    # Loudness trung bình
    A_avg = np.mean([bat.loudness for bat in population])
    for bat in population:
        # Điều kiện local search
        if np.random.rand() > bat.pulse_rate:
            epsilon = np.random.uniform(-1, 1, size=len(bat.position))
            new_position = x_best + epsilon * A_avg
            # Giữ trong bounds
            bat.position = np.clip(new_position, lb, ub)

def selection_and_update(population, objective_function,
                         best_solution, best_fitness,
                         iteration,
                         alpha=0.9, gamma=0.9):
   
    for bat in population:
        # Fitness của nghiệm hiện tại
        fitness_new = objective_function(bat.position)
        # ------------------------------
        # ACCEPTANCE RULE
        # ------------------------------
        if (fitness_new <= bat.best_fitness) and (np.random.rand() < bat.loudness):
            # Chấp nhận nghiệm mới
            bat.best_position = bat.position.copy()
            bat.best_fitness = fitness_new
            # ------------------------------
            # UPDATE LOUDNESS
            # A(t+1) = alpha * A(t)
            # ------------------------------
            # old version: bat.loudness *= alpha
            bat.loudness = max(bat.loudness * alpha, 0.01) # clamp value to avoid zero


def local_random_walk_for_benchmark(population, x_best, bounds):
    lb, ub = bounds
    avg_loudness = np.mean([bat.loudness for bat in population])

    for bat in population:
        if np.random.rand() > bat.pulse_rate:
            epsilon = np.random.uniform(-1.0, 1.0, size=len(bat.position))
            bat.position = np.clip(x_best + epsilon * avg_loudness, lb, ub)

def improved_local_random_walk_for_benchmark(population, x_best, bounds):
    lb, ub = bounds
    avg_loudness = np.mean([bat.loudness for bat in population])

    for bat in population:
        if np.random.rand() > bat.pulse_rate:
            epsilon = np.random.uniform(-1.0, 1.0, size=len(bat.position))
            bat.position = bat.position + epsilon * avg_loudness

def selection_and_update_for_benchmark(population, objective_function,
                                       best_solution, best_fitness,
                                       iteration,
                                       alpha=0.95, gamma=0.9,
                                       behavior_mode="individual"):
    for bat in population:
        fitness_new = objective_function(bat.position)

        if (fitness_new <= bat.best_fitness) and (np.random.rand() < bat.loudness):
            bat.best_position = bat.position.copy()
            bat.best_fitness = fitness_new

        bat.fitness = fitness_new

        if bat.best_fitness < best_fitness:
            best_fitness = bat.best_fitness
            best_solution = bat.best_position.copy()

    update_behavior(population, iteration=iteration, alpha=alpha, gamma=gamma, mode=behavior_mode)
    return best_solution, best_fitness



    

