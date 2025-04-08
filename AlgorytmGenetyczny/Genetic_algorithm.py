import random
import math
import numpy as np

def f(x):
    return x**2 - 1

def Population(pop):
    """Create a population of individuals"""
    return [random.uniform(-pop, pop) for _ in range(pop)]


def Fitness(fun, args):
    results = []
    for arg in args:
        value = fun(arg)
        results.append({'arg': arg, 'value': value})

    # Sortujemy względem odległości od zera (moduł)
    results.sort(key=lambda x: abs(x['value']))
    return results

def Selection(population):
    """Select individuals for reproduction based on fitness"""
    selected = []
    temp = []
    if int(len(population) * 0.2) <= 0:
        maxLen = 1
    else:
        maxLen = int(len(population) * 0.2)
    length = int(len(population)/maxLen)
    print("Ilość truniejów: ", maxLen, " Ilość uczestików :", length)
    while len(selected) < maxLen:
        for i in range(0,length):
            index = random.randint(0, len(population) - 1)
            temp.append(population[index])
            population.remove(population[index])
        temp.sort(key=lambda x: abs(x['value']))
        selected.append(temp[0])
        temp = []
    return selected

import random

def Crossover(population, mutation_rate=0.01, reproduction_rate=1):
    """Perform crossover between two parents."""
    length = len(population)
    new_population = []
    
    # Ensure the population is not modified while iterating
    population_copy = population[:]
    
    for i in range(length):
        if(random.uniform(0,1) < 0.1):
            continue    
        main = population_copy.pop(0)  # Select the main parent
        
        # Perform reproduction (create new candidate children)
        candidates = []
        for a in range(reproduction_rate):
            candidate = population[random.randint(0, len(population)-1)]
            candidates.append(candidate)
        
        # Now perform crossover with each candidate
        for candidate in candidates:
            arg1 = candidate['arg']
            arg2 = main['arg']
            
            # Perform mutation on arg1 with probability mutation_rate
            if random.random() < mutation_rate:
                arg1 = arg1 * random.uniform(0.01, 0.99)

            # Perform mutation on arg2 with probability mutation_rate
            if random.random() < mutation_rate:
                arg2 = arg2 * random.uniform(0.01, 0.99)

            # Crossover: average the two arguments
            arg = (arg1 + arg2) / 2
            
            # Evaluate the fitness function (if provided)
            if f:
                val = f(arg)
            else:
                val = 0  # Placeholder, assume zero if no fitness function is provided
            
            # Create the child and add to the population
            child = {'arg': arg, 'value': val}
            new_population.append(child)
        
        # Add the main parent back into the population
        new_population.append(main)
    
    # Sort the population based on fitness (assuming 'value' is the fitness score)
    new_population.sort(key=lambda x: abs(x['value']))
    return new_population



def Genetic_algorithm(population_size, f, max_generations, mutation_rate=0.01 , eps=0.01):
    """Genetic algorithm to optimize the function f(x)"""
    population = Population(population_size)
    i = 0
    newPopulation = []
    population = Fitness(f, population)
    while i < max_generations:
        print("Pokolenie: ", i," Wielkość populacji: ", len(population), " Wielkość nowej populacji: ", len(newPopulation), " \ " , int(len(population)*0.2) )
        i += 1
        #print("Najlepszy osobnik: ", population[0]['arg'])
        #print("Wartość: ", population[0]['value'])
        newPopulation = Selection(population)
        population = Crossover(newPopulation, mutation_rate, 5)
        if(abs(population[0]['value']) < eps):
            print("Znaleziono rozwiązanie: ", population[0]['arg'])
            break
    return population







Mutation_rate = 0.01
Max_generations = 1000
Population_size = 20

res = Genetic_algorithm(Population_size, f, Max_generations, Mutation_rate)
res.sort(key=lambda x: abs(x['value']))
print("Najlepsze osobniki:")
print("\tARG\t\t\tWARTOŚĆ")
for i in range(int(len(res)*0.2)):
    print(res[i]['arg'],'\t', res[i]['value'])