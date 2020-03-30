import math
import random
import numpy.random as npr

p_mutation = 0.20
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness, queens):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)
        new_population = set()
        for i in range((len(population))):

            mother, father = random_selection(population, fitness_fn)
            children = reproduce(mother, father, queens)
            if random.uniform(0, 1) < p_mutation:
                children = mutate(children, queens)

            for child in children:
                new_population.add(child)
            new_population.add(mother)
            new_population.add(father)
        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father, queens):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    crossover = random.randint(1, queens - 2)
    child1 = mother[:crossover] + father[crossover:]
    child2 = father[:crossover] + mother[crossover:]
    return [child1, child2]


def mutate(children, queens):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    mutations = []
    for child in children:
        mutatepoint = random.randint(0, queens - 1)
        mutation = child[:mutatepoint] + (random.randint(1, 8),) + child[mutatepoint + 1:]
        mutations.append(mutation)
    return mutations


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """
    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    ordered_population = list(population)
    fitness_list = []
    selected = []
    total_fitness = 0
    # for individ in ordered_population:
    # fitness = fitness_fn(individ)
    # total_fitness += fitness
    # fitness_list.append(total_fitness)
    # Make roulette wheel selection
    max = sum([fitness_fn(c) for c in ordered_population])
    while len(selected) != 2:
        selection_probs = [fitness_fn(c) / max for c in ordered_population]
        selected.append(ordered_population[npr.choice(len(ordered_population), p=selection_probs)])

        # for fitness in fitness_list:
        # if roulettepoint <= fitness:
        # selected.append(ordered_population[popindex])
        # break
        # popindex += 1

    return selected


def fitness_fn_negative(individual):
    '''
    Compute the number of conflicting pairs, negated.
    For a solution with 5 conflicting pairs the return value is -5, so it can
    be maximized to 0.
    '''

    n = len(individual)
    fitness = 0
    for column, row in enumerate(individual):
        contribution = 0

        # Horizontal
        for other_column in range(column + 1, n):
            if individual[other_column] == row:
                contribution += 1

        # Diagonals
        for other_column in range(column + 1, n):
            row_a = row + (column - other_column)
            row_b = row - (column - other_column)
            if 0 <= row_a < n and individual[other_column] == row_a:
                contribution += 1
            if 0 <= row_b < n and individual[other_column] == row_b:
                contribution += 1

        fitness += contribution

    return - fitness


def fitness_fn_positive(state):
    '''
    Compute the number of non-conflicting pairs.
    '''

    def conflicted(state, row, col):
        for c in range(col):
            if conflict(row, col, state[c], c):
                return True

        return False

    def conflict(row1, col1, row2, col2):
        return (
                row1 == row2 or
                col1 == col2 or
                row1 - col1 == row2 - col2 or
                row1 + col1 == row2 + col2
        )

    fitness = 0
    for col in range(len(state)):
        for pair in range(1, col + 1):
            if not conflicted(state, state[pair], pair):
                fitness = fitness + 1
    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    queens = 8
    minimal_fitness = (queens * (queens - 1)) / 2
    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (7, 1, 6, 5, 8, 1, 6, 5),
        (5, 8, 3, 1, 2, 4, 1, 7),
        (1, 7, 6, 8, 1, 2, 6, 8),
        (8, 3, 1, 5, 8, 7, 2, 1),

        # (7, 1, 6, 5, 8, 1, 6),
        # (5, 8, 3, 1, 2, 4, 1),
        # (1, 7, 6, 8, 1, 2, 6),
        # (8, 3, 1, 5, 8, 7, 2),
        #
        # (7, 1, 6, 5, 8, 1),
        # (5, 8, 3, 1, 2, 4),
        # (1, 7, 6, 8, 1, 2),
        # (8, 3, 1, 5, 8, 7)

    }

    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_fn_positive, minimal_fitness, queens)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()
