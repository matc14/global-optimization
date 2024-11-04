import math
import random

def rastrigin_function(xi):
    sum = 0
    for x in xi:
        sum += x**2 - 10 * math.cos(20 * math.pi * x)
    return 10 * len(xi) + sum


def calculate_binary_length(a, b, d):
    m_list = []
    c_list = []
    for i in range(len(a)):
        m = 0
        c = (b[i] - a[i]) * 10**d[i] + 1
        while 2**m < (b[i] - a[i]) * 10**d[i] or 2**(m - 1) > (b[i] - a[i]) * 10**d[i]:
            m += 1
        m_list.append(m)
        c_list.append(c)
    return m_list, c_list


def generate_population(n, m_list, c_list):
    all_populations = []

    for i in range(len(m_list)):
        m = m_list[i]
        c = c_list[i]
        population = set()
        while len(population) < n:
            random_number = random.randint(0, c - 1)
            binary_value = bin(random_number)[2:].zfill(m)
            population.add(binary_value)
        all_populations.append(list(population))

    combined_population = []
    for i in range(n):
        combined_individual = ''.join(population[i] for population in all_populations)
        combined_population.append(combined_individual)

    # print(all_populations)
    # print(combined_population)
    return all_populations, combined_population


def evaluate_population(populations, a_list, b_list, m_list):
    evaluated_populations = []

    for pop_idx, population in enumerate(populations):
        a = a_list[pop_idx]
        b = b_list[pop_idx]
        m = m_list[pop_idx]

        decimal = [int(p, 2) for p in population]

        in_range_ab = [a + ((b - a) * d) / (2**m - 1) for d in decimal]

        evaluated_populations.append(in_range_ab)

    transposed_population = list(map(list, zip(*evaluated_populations)))

    rastrigin_results = []
    for column in transposed_population:
        rastrigin_result = rastrigin_function(column)
        rastrigin_results.append(rastrigin_result)

    return rastrigin_results


def genetic_algorithm(a, b, d):
    m, c = calculate_binary_length(a, b, d)
    populations, chromosomes = generate_population(10, m, c)
    values = evaluate_population(populations, a, b, m)
    combined = list(zip(chromosomes, values))
    return combined


def tournament_selection(population, minimize=False, replacement=False):
    winners = []
    compare = min if minimize else max
    il = len(population)

    print("Groups:")
    for _ in range(il):
        if replacement:
            tournament_group = random.choices(population, k=2)
        else:
            tournament_group = random.sample(population, k=2)
        print(tournament_group)
        
        winner = compare(tournament_group, key=lambda x: x[1])
        winners.append(winner)
        
    print("Result:")
    return winners


def ranking_selection(population, minimize=False):
    winners = []
    sorting = False if minimize else True
    il = len(population)
    sorted_population = sorted(population, key=lambda x: x[1], reverse=sorting)
    print("Sorted population:")
    print(sorted_population)
    for _ in range(il):
        first_random = random.randint(0, il - 1)
        second_random = random.randint(0, first_random)
        winner = sorted_population[second_random]
        winners.append(winner)
    
    print("Result:")
    return winners


def roulette_selection(population, minimize=False):
    winners = []
    il = len(population)

    chromosomes = [value[0] for value in population]
    values = [value[1] for value in population]
    
    if minimize:
        inverted_values = [1 / value for value in values]
        total_value = sum(inverted_values)
        probabilities = [inv_value / total_value for inv_value in inverted_values]
    else:
        total_value = sum(values)
        probabilities = [value / total_value for value in values]

    distributions = []
    distribution = 0
    for prob in probabilities:
        distribution += prob
        distributions.append(distribution)
    print("Probability")
    print(probabilities)
    print("\nDistribution:")
    print(distributions)
    for _ in range(il):
        random_value = random.random()
        previous_distribution = 0
        for i, distribution in enumerate(distributions):
            if previous_distribution < random_value <= distribution:
                winners.append((chromosomes[i], values[i]))
                break
            previous_distribution = distribution
    print("\nResult:")
    return winners


def mutate_population(population, mutation_probability=0.2):
    mutated_population = []

    for chromosome, fitness in population:
        mutated_chromosome = ""
        for gene in chromosome:
            random_value = random.random()
            if random_value < mutation_probability:
                mutated_gene = '1' if gene == '0' else '0'
            else:
                mutated_gene = gene

            mutated_chromosome += mutated_gene

        mutated_population.append((mutated_chromosome, fitness))

    return mutated_population


def inverse_population(population, inversion_probability=0.2):
    inverted_population = []

    for chromosome, fitness in population:
        random_value = random.random()
        if random_value < inversion_probability:
            idx1, idx2 = sorted(random.sample(range(len(chromosome)), 2))
            inverted_chromosome = (
                    chromosome[:idx1] +
                    chromosome[idx1:idx2 + 1][::-1] +
                    chromosome[idx2 + 1:]
            )
        else:
            inverted_chromosome = chromosome

        inverted_population.append((inverted_chromosome, fitness))

    return inverted_population


def crossover_selection(population, crossover_probability=0.5):
    selected_population = []

    for chromosome, fitness in population:
        random_value = random.random()
        if random_value < crossover_probability:
            selected_population.append((chromosome, fitness))
    
    if len(selected_population) % 2 != 0:
        random_index = random.randint(0, len(selected_population) - 1)
        selected_population.remove(selected_population[random_index])

    random.shuffle(selected_population)
    crossover_pairs = [(selected_population[i], selected_population[i + 1])
             for i in range(0, len(selected_population) - 1, 2)]

    return crossover_pairs


def multipoint_crossover(pairs, crossover_type='single'):
    children = []
    
    for pair in pairs:
        (parent1, _), (parent2, _) = pair

        if crossover_type == 'single':
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]

        elif crossover_type == 'double':
            point1 = random.randint(1, len(parent1) - 2)
            point2 = random.randint(point1 + 1, len(parent1) - 1)
            child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
            child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        elif crossover_type == 'multi':
            points = random.randint(2,len(parent1) - 1)
            crossover_points = sorted(random.sample(range(1, len(parent1)), points))
            segments1, segments2 = [], []
            last_point = 0

            for i, point in enumerate(crossover_points + [len(parent1)]):
                if i % 2 == 0:
                    segments1.append(parent1[last_point:point])
                    segments2.append(parent2[last_point:point])
                else:
                    segments1.append(parent2[last_point:point])
                    segments2.append(parent1[last_point:point])
                last_point = point

            child1 = '|'.join(segments1)
            child2 = '|'.join(segments2)

        else:
            raise ValueError("Invalid crossover type or points for crossover.")

        children.append((child1, child2))

    return children


def uniform_crossover(pairs):
    children = []
    
    for pair in pairs:
        (parent1, _), (parent2, _) = pair

        pattern = ''.join(random.choice('01') for _ in range(len(parent1)))
        child1 = ''.join(parent1[i] if pattern[i] == '0' else parent2[i] for i in range(len(parent1)))
        child2 = ''.join(parent2[i] if pattern[i] == '0' else parent1[i] for i in range(len(parent1)))

        children.append((child1, child2))

    return children



A = [-1, 1, 1, 1]
B = [1, 3, 4, 4]
D = [1, 1, 1, 2]

population = genetic_algorithm(A, B, D)

# print("Initial population:")
# print(population)
# print("\nTournament selection:")
# print(tournament_selection(population, minimize=False, replacement=True))
# 
# print("Initial population:")
# print(population)
# print("\nRanking selection:")
# print(ranking_selection(population, minimize=False))
# 
# print("Initial population:")
# print(population)
# print("\nRoulette selection:")
# print(roulette_selection(population, minimize=False))
# 
# print("Mutation")
# print(mutate_population(population))
# 
# print("Inversion")
# print(inverse_population(mutate_population(population)))
#
# crossover_pairs = crossover_selection(population)
# print(crossover_pairs)
# print(multipoint_crossover(crossover_pairs, crossover_type='multi'))
# print(uniform_crossover(crossover_pairs))
