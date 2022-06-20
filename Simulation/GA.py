# 1 ferq (2?), 2 amplitudes, 2 phases
# maximum human walking speed 2.5 m/s with step of 80 cm => 3 steps/s
# 2 steps per priod => 1.5 Hz
# 1.5 > freq 1 > 0
# ferq 2 = 2*ferq 1
# pi/4 > amplitud2 > amplitud1 > 0 
# pi/2 > phase 2 > -pi/2
# pi/2 > phase 1 > -pi/2

import pygad
import numpy as np
import threading
from time import sleep
from math import pi
import random

cb_generation = None
cb_fitness = None

def fitness_func(solution, solution_idx):
    global cb_fitness
    return cb_fitness(solution, solution_idx)

# run new generation until time_per_gen seconds has passed, then return from generation_func with fitness_scores
def generation_func(instance):
    global cb_generation
    cb_generation(instance)

class GA:
    def __init__(self, generations, gen_time, population_size, callback_generation, callback_fitness, initial_genes = [0.25, 10*pi/180, 20*pi/180, -pi/2, -pi/2]):
        global time_per_gen, cb_generation, cb_fitness

        cb_generation = callback_generation
        cb_fitness = callback_fitness

        num_generations = generations
        num_parents_mating = population_size // 10

        population = np.array([])
        gene_space = [{'low': 0, 'high': 2}, {'low': 0, 'high': pi/4}, {'low': -pi/4, 'high': pi/4}, {'low': -pi/2, 'high': pi/2}, {'low': -pi/2, 'high': pi/2}]
        for _ in range(population_size):
            population = np.concatenate((population, np.array(
                initial_genes)))
        
        population = population.reshape(population_size, len(initial_genes))

        parent_selection_type = "rank"
        keep_parents = -1
        crossover_type = "uniform"
        mutation_type = "random"
        mutation_probability = 0.2
        
        self.ga = None
        self.ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            fitness_func=fitness_func,
                            initial_population=population,
                            parent_selection_type=parent_selection_type,
                            keep_parents=keep_parents,
                            crossover_type=crossover_type,
                            mutation_type=mutation_type,
                            mutation_probability=mutation_probability,
                            on_generation=generation_func,
                            delay_after_gen=gen_time,
                            gene_space=gene_space)

    def run(self):
        self.ga = threading.Thread(target=self.ga_instance.run)
        self.ga.start()

    def results(self):
        if self.ga is not None:
            self.ga.join()
        
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        self.ga_instance.plot_fitness()
