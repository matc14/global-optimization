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
        combined_individual = '|'.join(population[i] for population in all_populations)
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

    #print("Groups:")
    for _ in range(il):
        if replacement:
            tournament_group = random.choices(population, k=2)
        else:
            tournament_group = random.sample(population, k=2)
        #print(tournament_group)
        
        winner = compare(tournament_group, key=lambda x: x[1])
        winners.append(winner)
        
    #print("Result:")
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


def join_chromosome(chromosome):
    """Łączy segmenty chromosomu w jeden ciąg znaków."""
    return ''.join(chromosome.split('|'))


def split_chromosome(chromosome, segment_lengths):
    """Dzieli chromosom na segmenty o podanych długościach."""
    segments = []
    start = 0
    for length in segment_lengths:
        segments.append(chromosome[start:start + length])
        start += length
    return '|'.join(segments)


def recalculate_fitness(population, a, b, m):
    chromosomes = [individual[0] for individual in population]
    split_chromosomes = [chromosome.split('|') for chromosome in chromosomes]
    all_populations = list(map(list, zip(*split_chromosomes)))
    new_values = evaluate_population(all_populations, a, b, m)
    updated_population = [(chromosomes[i], new_values[i]) for i in range(len(chromosomes))]
    return updated_population


def mutate_population(population, segment_lengths, mutation_probability=0.2):
    mutated_population = []

    for chromosome, fitness in population:
        full_chromosome = join_chromosome(chromosome)
        mutated_chromosome = ""
        for gene in full_chromosome:
            if random.random() < mutation_probability:
                mutated_gene = '1' if gene == '0' else '0'
            else:
                mutated_gene = gene
            mutated_chromosome += mutated_gene

        final_chromosome = split_chromosome(mutated_chromosome, segment_lengths)
        mutated_population.append((final_chromosome, fitness))

    return mutated_population


def inverse_population(population, segment_lengths, inversion_probability=0.2):
    inverted_population = []

    for chromosome, fitness in population:
        full_chromosome = join_chromosome(chromosome)
        if random.random() < inversion_probability:
            idx1, idx2 = sorted(random.sample(range(len(full_chromosome)), 2))
            full_chromosome = (
                    full_chromosome[:idx1] + full_chromosome[idx1:idx2 + 1][::-1] + full_chromosome[idx2 + 1:]
            )

        final_chromosome = split_chromosome(full_chromosome, segment_lengths)
        inverted_population.append((final_chromosome, fitness))

    return inverted_population


def crossover_selection(population, crossover_probability=0.5):
    selected_indices = []

    for i in range(len(population)):
        if random.random() < crossover_probability:
            selected_indices.append(i)

    if len(selected_indices) % 2 != 0:
        selected_indices.pop(random.randint(0, len(selected_indices) - 1))

    random.shuffle(selected_indices)
    crossover_pairs = [(selected_indices[i], selected_indices[i + 1])
                       for i in range(0, len(selected_indices), 2)]

    return crossover_pairs

def multipoint_crossover(population, pairs, segment_lengths, crossover_type='single'):

    for idx1, idx2 in pairs:
        parent1, fitness1 = population[idx1]
        parent2, fitness2 = population[idx2]

        parent1_full = join_chromosome(parent1)
        parent2_full = join_chromosome(parent2)
        length = len(parent1_full)

        if crossover_type == 'single':
            point = random.randint(1, length - 1)
            child1 = parent1_full[:point] + parent2_full[point:]
            child2 = parent2_full[:point] + parent1_full[point:]

        elif crossover_type == 'double':
            point1 = random.randint(1, length - 2)
            point2 = random.randint(point1 + 1, length - 1)
            child1 = parent1_full[:point1] + parent2_full[point1:point2] + parent1_full[point2:]
            child2 = parent2_full[:point1] + parent1_full[point1:point2] + parent2_full[point2:]

        elif crossover_type == 'multi':
            num_points = random.randint(3, length - 1)
            crossover_points = sorted(random.sample(range(1, length), num_points))
            segments1, segments2 = [], []
            last_point = 0

            for i, point in enumerate(crossover_points + [length]):
                if i % 2 == 0:
                    segments1.append(parent1_full[last_point:point])
                    segments2.append(parent2_full[last_point:point])
                else:
                    segments1.append(parent2_full[last_point:point])
                    segments2.append(parent1_full[last_point:point])
                last_point = point

            child1 = ''.join(segments1)
            child2 = ''.join(segments2)

        child1_split = split_chromosome(child1, segment_lengths)
        child2_split = split_chromosome(child2, segment_lengths)

        population[idx1] = (child1_split, fitness1)
        population[idx2] = (child2_split, fitness2)

    return population



def uniform_crossover(population, pairs, segment_lengths):
    for idx1, idx2 in pairs:
        parent1, fitness1 = population[idx1]
        parent2, fitness2 = population[idx2]

        parent1_full = join_chromosome(parent1)
        parent2_full = join_chromosome(parent2)

        pattern = ''.join(random.choice('01') for _ in range(len(parent1_full)))
        child1 = ''.join(parent1_full[i] if pattern[i] == '0' else parent2_full[i] for i in range(len(parent1_full)))
        child2 = ''.join(parent2_full[i] if pattern[i] == '0' else parent1_full[i] for i in range(len(parent1_full)))

        child1_split = split_chromosome(child1, segment_lengths)
        child2_split = split_chromosome(child2, segment_lengths)

        population[idx1] = (child1_split, fitness1)
        population[idx2] = (child2_split, fitness2)

    return population



A = [-1, 1, 1, 1]
B = [1, 3, 4, 4]
D = [1, 1, 1, 2]

population = genetic_algorithm(A, B, D)

segment_lengths = [len(segment) for segment in population[0][0].split('|')]


for epoch in range(10):
    print(f"\nEpoch {epoch + 1}")
    selected_population = tournament_selection(population)
    mutated_population = mutate_population(selected_population, segment_lengths)
    inverted_population = inverse_population(mutated_population, segment_lengths)
    crossover_pairs = crossover_selection(inverted_population)
    population = uniform_crossover(inverted_population, crossover_pairs, segment_lengths)
    population = recalculate_fitness(population, A, B, calculate_binary_length(A, B, D)[0])
    for chromosome in population:
        print(chromosome)
