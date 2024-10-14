import math
import random


def rastrigin_function(xi):
    sum = 0
    for x in xi:
        sum += x**2 - 10 * math.cos(20 * math.pi * x)
    return 10 * len(xi) + sum


def calculate_binary_length(a, b, d):
    m_list = []
    for i in range(len(a)):
        m = 0
        while 2**m < (b[i] - a[i]) * 10**d[i] or 2**(m - 1) > (b[i] - a[i]) * 10**d[i]:
            m += 1
        m_list.append(m)
    return m_list


def generate_population(n, m_list):
    all_populations = []

    for m in m_list:
        population = set()
        while len(population) < n:
            random_number = random.randint(0, 2**m - 1)
            binary_value = bin(random_number)[2:].zfill(m)
            population.add(binary_value)
        all_populations.append(list(population))

    combined_population = []
    for i in range(n):
        combined_individual = ''.join(population[i] for population in all_populations)
        combined_population.append(combined_individual)

    print(all_populations)
    print(combined_population)
    return all_populations


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
    m = calculate_binary_length(a, b, d)
    population = generate_population(10, m)
    result = evaluate_population(population, a, b, m)
    return result


A = [-1, 1, 1, 1]
B = [1, 3, 4, 4]
D = [1, 1, 1, 2]

print(genetic_algorithm(A, B, D))