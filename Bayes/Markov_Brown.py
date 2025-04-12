import numpy as np
import matplotlib.pyplot as plt

# Parametry
num_times = 30
mean0 = 0
var = 1
std = np.sqrt(var)

np.random.seed(42)

# PRZYPADEK 1: Niezależne zmienne
x_independent = np.random.normal(mean0, std, size=num_times)

# PRZYPADEK 2: Łańcuch Markowa (x[t-1])
x_markov = np.zeros(num_times)
x_markov[0] = np.random.normal(mean0, std)
for t in range(1, num_times):
    x_markov[t] = np.random.normal(x_markov[t - 1], std)

# PRZYPADEK 3: Markow z 2 poprzednich
x_markov2 = np.zeros(num_times)
x_markov2[0] = np.random.normal(mean0, std)
x_markov2[1] = np.random.normal(x_markov2[0], std)
for t in range(2, num_times):
    mean_t = 0.5 * (x_markov2[t - 1] + x_markov2[t - 2])
    x_markov2[t] = np.random.normal(mean_t, std)

# PRZYPADEK 4: Ruch Browna
increments = np.random.normal(0, std, size=num_times)
x_brownian = np.cumsum(increments)

# Funkcja pomocnicza do rysowania i zapisu
def plot_and_save(data, title, filename, color):
    plt.figure(figsize=(8, 4))
    plt.plot(data, marker='o', linestyle='-', color=color)
    plt.title(title)
    plt.xlabel('Czas t')
    plt.ylabel('x[t]')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Zapis wykresów do plików
plot_and_save(x_independent, 'Niezależne zmienne', 'independent.png', 'gray')
plot_and_save(x_markov, 'Łańcuch Markowa (x[t-1])', 'markov.png', 'royalblue')
plot_and_save(x_markov2, 'Rozszerzony Markow (x[t-1], x[t-2])', 'markov2.png', 'darkorange')
plot_and_save(x_brownian, 'Ruch Browna', 'brownian.png', 'green')
