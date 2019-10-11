#!/usr/bin/env python3

# Please feel free to modify any part of the code or add any functions, or modify the argument of the given functions. But please keep the name of the given functions

# Please feel free to import any libraries you need.

# You are required to finish the genetic_algorithm function, and you may need to complete crossover, mutate and select.

import random as rand
import matplotlib.pyplot as plt

def crossover(parents, probability_crossover, food_map, map_size, elite_degree): #using multi-point crossover
    #TODO START

    def calculate_fitness(gene): # same as ant_simulator but just returns fitness for ease of sorting and picking children by fitness
        trial, fitness = ant_simulator(food_map, map_size, gene)
        return fitness

    children = []

    parent_pairs = []
    for i in range(len(parents)):
        for j in range(i+1, len(parents)):
            parent_pairs.append([parents[i], parents[j]])

    all_children = []
    for pair in parent_pairs:
        child_1 = ""
        child_2 = ""
        for j in range(10):
            random = rand.random()
            if random <= probability_crossover:
                child_1 = child_1 + pair[1][3*j:3*j+3]
                child_2 = child_2 + pair[0][3*j:3*j+3]
            else:
                child_1 = child_1 + pair[0][3*j:3*j+3]
                child_2 = child_2 + pair[1][3*j:3*j+3]
        all_children.append(child_1)
        all_children.append(child_2)

    sorted_children = sorted(all_children, key=calculate_fitness, reverse=True) #sort all children by fitness and take greedily select the top
    for i in range(len(parents)):
        children.append(sorted_children[i])

    #TODO END
    return children

def mutate(children, probability_mutation):
    #TODO START
    new_gen = []
    
    for child in children:
        digit = 0
        while digit < 6:
            random = rand.random()
            if random <= probability_mutation:
                new_child = ""
                if digit % 3 == 0:
                    random = rand.randint(1, 4)
                else:
                    random = rand.randint(0, 9)
                new_child = child[:digit] + str(random) + child[digit+1:]
                child = new_child
            digit += 1
        new_gen.append(child)

    #TODO END
    return new_gen

def select(sorted_old_gen, elite_degree): # combination of rank selection and elitism
    #TODO START
    parents = []
    wheel = []

    for i in range(elite_degree):
        parents.append(sorted_old_gen[-i-1])

    for i in range(len(sorted_old_gen)):
        for j in range(i+1):
            wheel.append(sorted_old_gen[i])

    for i in range(len(sorted_old_gen)-elite_degree):
        random = rand.randint(0, len(wheel)-1)
        parents.append(wheel[random])

    #TODO END
    return parents

def genetic_algorithm(population, food_map_file_name, max_generation, probability_crossover, probability_mutation, elite_degree):
    #TODO START
    stats = []
    max_fitness = -1
    max_individual = ""
    max_trial = ""
    food_map, map_size = get_map(food_map_file_name)
    new_pop = population
    current_fitnesses = []
    current_gen = 0

    def calculate_fitness(gene): # same as ant_simulator but just returns fitness for ease of sorting and generating rank selection wheel
        trial, fitness = ant_simulator(food_map, map_size, gene)
        return fitness

    for individual in population:
        current_fitnesses.append(calculate_fitness(individual))
        stats.append([max(current_fitnesses), min(current_fitnesses), sum(current_fitnesses)/len(current_fitnesses)])

    while (current_gen < max_generation):
        sorted_pop = sorted(new_pop, key=calculate_fitness)
        parents = select(sorted_pop, elite_degree)
        children = crossover(parents, probability_crossover, food_map, map_size, elite_degree)
        new_pop = mutate(children, probability_mutation)

        current_fitnesses = []
        for individual in new_pop:
            current_fitnesses.append(calculate_fitness(individual))

        stats.append([max(current_fitnesses), min(current_fitnesses), sum(current_fitnesses)/len(current_fitnesses)])

        current_gen += 1
    
    max_individual = max(new_pop, key=calculate_fitness)
    max_trial, max_fitness = ant_simulator(food_map, map_size, max_individual)
    population = new_pop

    return max_fitness, max_individual, max_trial, stats, population
    #TODO END    

def initialize_population(num_population):
    #TODO START
    population = []
    
    for i in range(num_population): # create a population of random genes
        gene = ""
        for j in range(30):
            if j % 3 == 0:
                random = rand.randint(1,4) # making sure that every 1st digit in each triplet is between 1 and 4
            else:
                random = rand.randint(0,9)
            gene = gene + str(random)
        population.append(gene)

    #TODO END
    return population
    
def ant_simulator(food_map, map_size, ant_genes):
    """
    parameters:
        food_map: a list of list of strings, representing the map of the environment with food
            "1": there is a food at the position
            "0": there is no food at the position
            (0, 0) position: the top left corner of the map
            (x, y) position: x is the row, and y is the column
        map_size: a list of int, the dimension of the map. It is in the format of [row, column]
        ant_genes: a string with length 30. It encodes the ant's genes, for more information, please refer to the handout.
    
    return:
        trial: a list of list of strings, representing the trials
            1: there is food at that position, and the spot was not visited by the ant
            0: there is no food at that position, and the spot was not visited by the ant
            empty: the spot has been visited by the ant
    
    It takes in the food_map and its dimension of the map and the ant's gene information, and return the trial in the map
    """
    
    step_time = 200
    
    trial = []
    for i in food_map:
        line = []
        for j in i:
            line.append(j)
        trial.append(line)

    position_x, position_y = 0, 0
    orientation = [(1, 0), (0, -1), (-1, 0), (0, 1)] # face down, left, up, right
    fitness = 0
    state = 0
    orientation_state = 3
    gene_list = [ant_genes[i : i + 3] for i in range(0, len(ant_genes), 3)]
    
    for i in range(step_time):
        if trial[position_x][position_y] == "1":
            fitness += 1
        trial[position_x][position_y] = " "
        
        sensor_x = (position_x + orientation[orientation_state][0]) % map_size[0]
        sensor_y = (position_y + orientation[orientation_state][1]) % map_size[1]
        sensor_result = trial[sensor_x][sensor_y]
        
        if sensor_result == "1":
            state = int(gene_list[state][2])
        else:
            state = int(gene_list[state][1])
        
        action = gene_list[state][0]
        
        if action == "1": # move forward
            position_x = (position_x + orientation[orientation_state][0]) % map_size[0]
            position_y = (position_y + orientation[orientation_state][1]) % map_size[1]
        elif action == "2": # turn right
            orientation_state = (orientation_state + 1) % 4
        elif action == "3": # turn left
            orientation_state = (orientation_state - 1) % 4
        elif action == "4": # do nothing
            pass
        else:
            raise Exception("invalid action number!")
    
    return trial, fitness
        

def get_map(file_name):
    """
    parameters:
        file_name: a string, the name of the file which stored the map. The first line of the map is the dimension (row, column), the rest is the map
            1: there is a food at the position
            0: there is no food at the position
    
    return:
        food_map: a list of list of strings, representing the map of the environment with food
            "1": there is a food at the position
            "0": there is no food at the position
            (0, 0) position: the top left corner of the map
            (x, y) position: x is the row, and y is the column
        map_size: a list of int, the dimension of the map. It is in the format of [row, column]
    
    It takes in the file_name of the map, and return the food_map and the dimension map_size
    """
    food_map = []
    map_file = open(file_name, "r")
    first_line = True
    map_size = []
    
    for line in map_file:
        line = line.strip()
        if first_line:
            first_line = False
            map_size = line.split()
            continue
        if line:
            food_map.append(line.split())
    
    map_file.close()
    return food_map, [int(i) for i in map_size]

def display_trials(trials, target_file):
    """
    parameters:
        trials: a list of list of strings, representing the trials
            1: there is food at that position, and the spot was not visited by the ant
            0: there is no food at that position, and the spot was not visited by the ant
            empty: the spot has been visited by the ant
        taret_file: a string, the name the target_file to be saved
    
    It takes in the trials, and target_file, and saved the trials in the target_file. You can open the target_file to take a look at the ant's trial.
    """
    trial_file = open(target_file, "w")
    for line in trials:
        trial_file.write(" ".join(line))
        trial_file.write("\n")
    trial_file.close()

if __name__ == "__main__":
    #TODO START
    #You will need to modify the parameters below.
    #The parameters are for references, please feel free add more or delete the ones you do not intend to use in your genetic algorithm
    
    population_size = 30
    population = initialize_population(population_size)
    food_map_file_name = "muir.txt"
    max_generation = 200
    probability_crossover = 0.75
    probability_mutation = 0.02
    elite_degree = 10
    max_fitness, max_individual, max_trial, stats, population = genetic_algorithm(population, food_map_file_name, max_generation, probability_crossover, probability_mutation, elite_degree)
    display_trials(max_trial, "max_trial.txt")
    
    plt.figure(1)
    plt.plot([i for i in range(len(stats))], [i[0] for i in stats], marker = "o")
    plt.xlabel("generation")
    plt.xlim((0, max_generation))
    plt.ylim((0, max(i[0] for i in stats) + 10))
    plt.ylabel("most fit individual")
    plt.savefig("max fitness of each generation.png")
    
    plt.figure(2)
    muir_fitness = []
    santafe_fitness = []
    muir_food_map, muir_map_size = get_map("muir.txt")
    santafe_food_map, santafe_map_size = get_map("santafe.txt")
    for individual in population:
        trial, individual_muir_fitness = ant_simulator(muir_food_map, muir_map_size, individual)
        trial, individual_santafe_fitness = ant_simulator(santafe_food_map, santafe_map_size, individual)
        muir_fitness.append(individual_muir_fitness)
        santafe_fitness.append(individual_santafe_fitness)
    
    plt.plot([i for i in range(len(muir_fitness))], muir_fitness, marker = "o", color = "blue", label = "muir")
    plt.plot([i for i in range(len(santafe_fitness))], santafe_fitness, marker = "o", color = "green", label = "santa fe")
    plt.xlabel("individuals in the last generation")
    plt.xlim((0, population_size))
    plt.ylim((0, max(muir_fitness + santafe_fitness) + 10))
    plt.ylabel("fitness")
    plt.legend()
    plt.savefig("fitness of last generation on muir and santa fe map.png")
    
    #TODO END
    
    # Example of how to use get_map, ant_simulator and display trials function
    """
    food_map, map_size = get_map("muir.txt")
    ant_genes = "335149249494173115455311387263"
    trial, fitness = ant_simulator(food_map, map_size, ant_genes)
    display_trials(trial, "trial.txt")
    """