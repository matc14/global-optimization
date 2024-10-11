import math
import random

# def rastrigin_function(xi):
#     sum = 0
#     for x in xi:
#         sum += x**2 - 10 * math.cos(20 * math.pi * x)
#     return 10 * len(xi) + sum

def genetic_algorithm_1d(a, b, d):
    m = calculate_binary_length(a, b, d)
    population = generate_population(10, m)
    result = evaluate_population(population, a, b, m)
    return result

def rastrigin_function_1d(x):
    return 10 + x**2 - 10 * math.cos(20 * math.pi * x)

def calculate_binary_length(a, b, d):
    m = 1
    while 2**m < (b - a) * 10**d or 2**(m - 1) > (b - a) * 10**d:
        m += 1
    return m

def generate_population(n, m):
    population = set()

    while len(population) < n:
        random_number = random.randint(0, 2**m - 1)
        binary_value = bin(random_number)[2:].zfill(m)
        population.add(binary_value)

    return list(population)

def evaluate_population(population, a, b, m):
    decimal = [int(p, 2) for p in population]
    in_range_ab = [a + ((b - a) * d) / (2**m - 1) for d in decimal]
    rastrigin = [rastrigin_function_1d(i) for i in in_range_ab]

    return rastrigin

print(genetic_algorithm_1d(-1, 1, 1))