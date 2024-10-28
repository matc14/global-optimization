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

    print(all_populations)
    print(combined_population)
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

    for _ in range(il):
        if replacement:
            tournament_group = random.choices(population, k=2)
        else:
            tournament_group = random.sample(population, k=2)

        winner = compare(tournament_group, key=lambda x: x[1])
        winners.append(winner)
    return winners

def ranking_selection(population, minimize=False):
    winners = []
    sorting = False if minimize else True
    il = len(population)
    sorted_population = sorted(population, key=lambda x: x[1], reverse=sorting)

    for _ in range(il):
        first_random = random.randint(0, il - 1)
        second_random = random.randint(0, first_random)
        winner = sorted_population[second_random]
        winners.append(winner)

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
    for _ in range(il):
        random_value = random.random()
        previous_distribution = 0
        for i, distribution in enumerate(distributions):
            if previous_distribution < random_value <= distribution:
                winners.append((chromosomes[i], values[i]))
                break
            previous_distribution = distribution

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
            print(idx1, idx2)
            inverted_chromosome = (
                    chromosome[:idx1] +
                    chromosome[idx1:idx2 + 1][::-1] +
                    chromosome[idx2 + 1:]
            )
        else:
            inverted_chromosome = chromosome

        inverted_population.append((inverted_chromosome, fitness))

    return inverted_population


    
A = [-1, 1, 1, 1]
B = [1, 3, 4, 4]
D = [1, 1, 1, 2]

population = genetic_algorithm(A, B, D)
print(population)

# print(tournament_selection(population, minimize=True ,replacement=True))
# print(ranking_selection(population, minimize=True))
# print(roulette_selection(population, minimize=True))

print(mutate_population(population))
print(inverse_population(population))
