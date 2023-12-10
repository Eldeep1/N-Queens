import numpy as np
genetic_queue = []
temp_individual = []

def init_pop(pop_size, board_size):
     return np.random.randint(board_size, size=(pop_size, board_size))

def calc_fitness(population, board_size):
        fitness_vals = []
        for x in population:
            penalty = 0
            for i in range(board_size):
                r = x[i]
                for j in range(board_size):
                    if i == j:
                        continue
                    d = abs(i - j)
                    if x[j] in [r, r - d, r + d]:
                        penalty += 1
            fitness_vals.append(penalty)
        return -1 * np.array(fitness_vals)

def selection(population, fitness_vals):
        probs = fitness_vals.copy()
        probs += abs(probs.min()) + 1
        probs = probs / probs.sum()
        N = len(population)
        indices = np.arange(N)
        selected_indices = np.random.choice(indices, size=N, p=probs)
        selected_population = population[selected_indices]
        return selected_population

def crossover(board_size, parent1, parent2, pc):
        r = np.random.random()
        if r < pc:
            m = np.random.randint(1, board_size)
            child1 = np.concatenate([parent1[:m], parent2[m:]])
            child2 = np.concatenate([parent2[:m], parent1[m:]])
        else:
            child1 = parent1.copy()
            child2 = parent2.copy()
        return child1, child2

def mutation(board_size, individual, pm):
        r = np.random.random()
        if r < pm:
            m = np.random.randint(board_size)
            individual[m] = np.random.randint(board_size)
        return individual


def crossover_mutation(board_size, selected_pop, pc, pm):
        N = len(selected_pop)
        new_pop = np.empty((N, board_size), dtype=int)
        for i in range(0, N, 2):
            parent1 = selected_pop[i]
            parent2 = selected_pop[i + 1]
            child1, child2 = crossover(board_size, parent1, parent2, pc)
            new_pop[i] = child1
            new_pop[i + 1] = child2
        for i in range(N):
            mutation(board_size, new_pop[i], pm)
        return new_pop
#########################################################################################
            
