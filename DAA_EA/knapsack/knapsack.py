import random

INIT_POPULATION = 100
MUTATION_PROBABILITY = 0.1
RECOMBINATION_PROBABILITY = 0.7

class Item():
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def load_input():
    first_line = True
    items = []
    with open('input', 'r') as file:
        lines = file.read().split('\n')
        for line in lines:
            values = line.split()
            if first_line:
                n, W = int(values[0]), int(values[1])
                first_line = False
            else:
                items.append(Item(int(values[0]), int(values[1])))
    return n,W, items

def calculate_fitness(genotype, items):
    fitness = 0
    for i in range(len(genotype)):
        fitness += genotype[i] * items[i].value
    return fitness

def init_population(n, items):
    population = []
    for _ in range(INIT_POPULATION):
        ids = [i for i in range(n)]
        random.shuffle(ids)
        weight = 0
        genotype = [0] * n
        for i in ids:
            if weight + items[i].weight <= W:
                genotype[i] = 1
                weight += items[i].weight
        population.append((calculate_fitness(genotype, items), genotype))
    return population

def check_weight(genotype, items):
    total_weight = 0
    included = []
    for i in range(len(genotype)):
        total_weight += genotype[i] * items[i].weight
        if genotype[i] == 1:
            included.append(i)
    if total_weight <= W:
        return genotype
    else:
        index = random.sample(included, 1)[0]
        genotype[index] = 0
        return check_weight(genotype, items)

def choose_parent(population):
    candidates = random.sample(population, 2)
    candidates = sorted(candidates, reverse=True)
    parent = candidates[0][1]
    return parent

def recombine(n, father, mother):
    if random.uniform(0, 1) <= RECOMBINATION_PROBABILITY:
        child1 = []
        child2 = []
        for i in range(n // 2 + 1):
            child1.append(father[1])
            child2.append(mother[1])
        for i in range(n // 2 + 1, n):
            child1.append(mother[i])
            child2.append(father[i])
        return child1, child2
    else:
        return father, mother

def mutate(genotype):
    if random.uniform(0, 1) <= MUTATION_PROBABILITY:
        genotype[random.randint(0, n - 1)] ^= 1
    genotype = check_weight(genotype, items)
    return genotype


if __name__ == '__main__':
    n, W, items = load_input()

    stop = False
    max_fitness = 0
    continuous_generation = 0
    max_genotype = None

    population = init_population(n, items)
    while not(stop):
        children = []
        while (len(children)<100):
            father = choose_parent(population)
            mother = choose_parent(population)
            child1, child2 = recombine(n, father, mother)
            child1 = mutate(child1)
            child2 = mutate(child2)

            children.append((calculate_fitness(child1, items), child1))
            children.append((calculate_fitness(child1, items), child2))

        population = children
        population = sorted(population, reverse=True)
        best_fitness, best_child = population[0]

        if best_fitness> max_fitness:
            max_fitness = best_fitness
            continuous_generation = 0
            max_genotype = best_child
        else:
            continuous_generation += 1

        if continuous_generation>25:
            stop = True

    print(max_fitness)
    print(max_genotype)