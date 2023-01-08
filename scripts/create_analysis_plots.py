import matplotlib.pyplot as plt
import numpy as np


def plot_sample():
    """
    Sample borrowed from matplotlib tutorial
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/fill_between_demo.html#sphx-glr-gallery-lines-bars-and-markers-fill-between-demo-py
    """
    N = 21
    x = np.linspace(0, 10, 11)

    y = [3.9, 4.4, 10.8, 10.3, 11.2, 13.1, 14.1, 9.9, 13.9, 15.1, 12.5]
    # fit a linear curve an estimate its y-values and their error.

    a, b = np.polyfit(x, y, deg=1)
    y_est = a * x + b
    y_err = x.std() * np.sqrt(1 / len(x) +
                              (x - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2))

    fig, ax = plt.subplots()
    ax.plot(x, y_est, '-')
    ax.fill_between(x, y_est - y_err, y_est + y_err, alpha=0.2)
    ax.plot(x, y, 'o', color='tab:brown')
    plt.grid(True)
    plt.show()


def plot_fitness_evolution():
    fit_max = [0.0, 0.05, 0.21, 0.33, 0.41, 0.55, 0.67, 0.75, 0.75, 0.75, 0.75, 0.75, 0.78, 0.78, 0.82] + 135 * [0.82]
    fit_avg = []
    fit_min = [0.0, 0.01, 0.02, 0.1, 0.15, 0.18] + (len(fit_max) - 6) * [0.18]

    x = np.arange(0.0, len(fit_max), 1.0)

    for i in range(len(fit_max)):
        fit_avg.append((fit_max[i] + fit_min[i]) / 2.0)

    fig, ax = plt.subplots()
    ax.plot(x, fit_avg, '-', color='tab:red', label="Mean Fitness")
    ax.fill_between(x, fit_max, fit_min, alpha=0.2, label="Min/Max Range")

    # ax.plot(x, fit_avg, 'o', color='tab:brown')
    plt.grid(True)
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    ax.legend()

    plt.show()

plot_sample()
plot_fitness_evolution()