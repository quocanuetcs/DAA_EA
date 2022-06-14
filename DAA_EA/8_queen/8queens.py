import random

POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.8
MAX_INTERATIONS = 1000

def calculate_fitness(individual):
    fitness = 28
    for x1 in range(8):
        y1 = individual[x1]
        for x2 in range(x1 + 1, 8):
            y2 = individual[x2]
            if x1 + y1 == x2 + y2 or x1 - y1 == x2 - y2:
                fitness -= 1
    return fitness

def init_population():
    population = []
    for _ in range(POPULATION_SIZE):
        individual = list(range(0, 8))
        random.shuffle(individual)
        population.append((calculate_fitness(individual), individual))
    return population

def select_parent(population):
    # Choose parents: Best 2 out of random 5
    candidates = random.sample(population, 5)
    candidates = sorted(candidates, reverse=True)
    return candidates[0][1], candidates[1][1]

def create_child(father, mother, pivot):
    child = []
    used = [False] * 8
    for i in range(pivot):
        child.append(father[i])
        used[father[i]] = True
    for i in range(8):
        if not used[mother[i]]:
            child.append(mother[i])
    return child

def recombine(father, mother):
    pivot = random.randint(0, 7)
    return create_child(father,mother, pivot), create_child(mother, father, pivot)

def mutate(individual):
    if random.uniform(0, 1) <= MUTATION_PROBABILITY:
        i, j = random.randint(0, 7), random.randint(0, 7)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def print_board(individual):
    for i in range(8):
        line = ''
        for j in range(8):
            line += '.' if j != individual[i] else 'Q'
        print(line)

if __name__ == '__main__':
    population = init_population()
    finded = False

    while MAX_INTERATIONS>0 and finded==False:
        MAX_INTERATIONS -= 1
        father, mother = select_parent(population)

        # Recombination
        child1, child2 = recombine(father, mother)

        # Mutation: swap
        child1 = mutate(child1)
        child2 = mutate(child2)

        population.append((calculate_fitness(child1), child1))
        population.append((calculate_fitness(child2), child2))

        population = sorted(population, reverse=True)
        population.pop()
        population.pop()

        best_fitness, best_child = population[0]
        print(best_fitness)
        if best_fitness == 28:
            finded = True

    best_fitness, best_child = max(population)
    if finded:
        print('Solution found!')
        print_board(best_child)
    else:
        print('Maximum evaluation reach. Current best fitness: {}'.format(best_fitness))
        print_board(best_child)
