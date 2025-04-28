# Algorytm genetyczny dla harmonogramowania zadan na wielu procesorach z zaleznosciami
import random
import copy
import heapq
from collections import defaultdict, deque

# Przykladowe dane
n_processors = 3

# Generowanie 100 zadan z losowymi zaleznosciami
processes = {}
num_tasks = 100

for i in range(num_tasks):
    task_id = f"T{i}"
    duration = random.randint(1, 10)
    if i == 0:
        deps = []
    else:
        # Kazde zadanie moze zalezec od maksymalnie 3 wczesniejszych
        num_deps = random.randint(0, min(3, i))
        deps = random.sample([f"T{j}" for j in range(i)], num_deps)
    processes[task_id] = {'duration': duration, 'deps': deps}

POPULATION_SIZE = 50
GENERATIONS = 200
MUTATION_RATE = 0.2

# Funkcja topologicznego sortowania

def topological_sort(processes):
    indegree = defaultdict(int)
    graph = defaultdict(list)
    for p, data in processes.items():
        for dep in data['deps']:
            graph[dep].append(p)
            indegree[p] += 1

    queue = deque([p for p in processes if indegree[p] == 0])
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order

# Generowanie poczatkowej populacji

def generate_initial_population(processes, size):
    population = []
    for _ in range(size):
        order = topological_sort(processes)
        random.shuffle(order)
        while not is_valid_order(order, processes):
            random.shuffle(order)
        assignment = {p: random.randint(0, n_processors - 1) for p in order}
        population.append((order, assignment))
    return population

# Sprawdzenie poprawnosci zaleznosci

def is_valid_order(order, processes):
    seen = set()
    for p in order:
        if not all(dep in seen for dep in processes[p]['deps']):
            return False
        seen.add(p)
    return True

# Oblicz harmonogram i makespan

def compute_schedule(order, assignment, processes):
    end_times = {}
    proc_times = [0] * n_processors

    for p in order:
        deps = processes[p]['deps']
        start_time = max([end_times[d] for d in deps] + [proc_times[assignment[p]]])
        end_time = start_time + processes[p]['duration']
        end_times[p] = end_time
        proc_times[assignment[p]] = end_time

    makespan = max(end_times.values())
    return makespan

# Selekcja turniejowa

def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])  # nizszy makespan = lepszy
    return selected[0][0]

# Krzyzowanie

def crossover(parent1, parent2):
    order1, assign1 = parent1
    order2, assign2 = parent2

    cut = random.randint(1, len(order1)-2)
    child_order = order1[:cut] + [p for p in order2 if p not in order1[:cut]]
    if not is_valid_order(child_order, processes):
        child_order = topological_sort(processes)

    child_assign = {p: assign1[p] if random.random() < 0.5 else assign2[p] for p in processes}
    return (child_order, child_assign)

# Mutacja

def mutate(individual):
    order, assign = individual
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(order)), 2)
        order[i], order[j] = order[j], order[i]
        if not is_valid_order(order, processes):
            order = topological_sort(processes)
    for p in assign:
        if random.random() < MUTATION_RATE:
            assign[p] = random.randint(0, n_processors - 1)
    return (order, assign)

# Glowna petla algorytmu genetycznego

def genetic_algorithm():
    population = generate_initial_population(processes, POPULATION_SIZE)
    best_solution = None
    best_fitness = float('inf')

    for gen in range(GENERATIONS):
        fitnesses = [compute_schedule(o, a, processes) for o, a in population]
        new_population = []
        for _ in range(POPULATION_SIZE):
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        gen_best = min(fitnesses)
        if gen_best < best_fitness:
            best_fitness = gen_best
            best_solution = population[fitnesses.index(gen_best)]
        print(f"Generacja {gen}, najlepszy makespan: {gen_best}")

    return best_solution, best_fitness

# Uruchom algorytm
best, fitness = genetic_algorithm()
print("\nNajlepsze rozwiazanie:")
print("Kolejnosc:", best[0])
print("Przypisanie procesorow:", best[1])
print("Makespan:", fitness)
