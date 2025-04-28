from collections import defaultdict
import random
import math


class Task:
    def __init__(self, name, time, dependencies=None):
        self.name = name
        self.time = time
        self.dependencies = dependencies if dependencies else []


def build_dependency_graph(tasks):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    task_map = {task.name: task for task in tasks}

    for task in tasks:
        for dep in task.dependencies:
            graph[dep].append(task.name)
            in_degree[task.name] += 1

        if task.name not in in_degree:
            in_degree[task.name] = 0

    return graph, in_degree, task_map


def generate_random_solution(tasks, m):
    graph, in_degree, task_map = build_dependency_graph(tasks)
    ready = [name for name, deg in in_degree.items() if deg == 0]
    random.shuffle(ready)

    sorted_tasks = []
    while ready:
        current = ready.pop()
        sorted_tasks.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                ready.append(neighbor)
                random.shuffle(ready)

    if len(sorted_tasks) != len(tasks):
        raise ValueError("Graf zależności zawiera cykl!")

    processors = [[] for _ in range(m)]
    for task_name in sorted_tasks:
        proc_id = random.randint(0, m - 1)
        processors[proc_id].append(task_name)

    return processors


def calculate_makespan(processors, task_map):
    end_times = [0] * len(processors)
    for i, proc in enumerate(processors):
        current_time = 0
        for task_name in proc:
            task_time = task_map[task_name].time
            current_time += task_time
        end_times[i] = current_time
    return max(end_times)


def generate_neighbor(processors, task_map, graph, in_degree):
    new_processors = [list(proc) for proc in processors]
    
    src_proc = random.randint(0, len(new_processors) - 1)
    if not new_processors[src_proc]:
        return new_processors  # procesor był pusty
    
    task_idx = random.randint(0, len(new_processors[src_proc]) - 1)
    task_name = new_processors[src_proc][task_idx]
    
    new_processors[src_proc].pop(task_idx)
    
    dst_proc = random.randint(0, len(new_processors) - 1)
    insert_idx = random.randint(0, len(new_processors[dst_proc]))
    new_processors[dst_proc].insert(insert_idx, task_name)
    
    return new_processors


def simulated_annealing(tasks, m, initial_temp, cooling_rate, max_iter):
    graph, in_degree, task_map = build_dependency_graph(tasks)
    current_solution = generate_random_solution(tasks, m)
    current_cost = calculate_makespan(current_solution, task_map)
    
    temp = initial_temp
    best_solution = current_solution
    best_cost = current_cost
    
    for i in range(max_iter):
        neighbor = generate_neighbor(current_solution, task_map, graph, in_degree)
        neighbor_cost = calculate_makespan(neighbor, task_map)
        
        if neighbor_cost < current_cost:
            current_solution = neighbor
            current_cost = neighbor_cost
            if neighbor_cost < best_cost:
                best_solution = neighbor
                best_cost = neighbor_cost
        else:
            prob = math.exp(-(neighbor_cost - current_cost) / temp)
            if random.random() < prob:
                current_solution = neighbor
                current_cost = neighbor_cost
        
        temp *= cooling_rate  # chłodzenie
    
    return best_solution, best_cost


def main():
    # Przykładowe zadania
    tasks = [
        Task('A', 3),
        Task('B', 2, ['A']),
        Task('C', 2, ['A']),
        Task('D', 4, ['B', 'C']),
        Task('E', 3, ['C']),
        Task('F', 1, ['D', 'E']),
    ]

    m = 2  # liczba procesorów
    initial_temp = 100
    cooling_rate = 0.95
    max_iter = 5000

    best_solution, best_cost = simulated_annealing(tasks, m, initial_temp, cooling_rate, max_iter)

    print("Najlepsze rozwiązanie (przydział zadań do procesorów):")
    for i, proc in enumerate(best_solution):
        print(f"Procesor {i+1}: {proc}")
    print(f"Czas zakończenia wszystkich zadań (makespan): {best_cost}")


if __name__ == "__main__":
    main()
