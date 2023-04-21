from random import randrange

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


def plot_fitness_evolution(evolutions: list = None):
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


def plot_fitness_per_dataset(title: str, axis_title: str, dataset_names: [], mean_std_dev_fit_values: [], path=""):
    N = len(np.array(mean_std_dev_fit_values)[:,0])
    ind = np.arange(N)
    width = 0.35

    fig = plt.subplots(figsize=(10, 7))
    plt.bar(ind, np.array(mean_std_dev_fit_values)[:,0], width, yerr=np.array(mean_std_dev_fit_values)[:,1])

    plt.ylabel(axis_title)
    plt.title(title)
    # plt.xticks(ind, ('T1', 'T2', 'T3', 'T4', 'T5'))
    # plt.yticks(np.arange(0, 81, 10))

    if path == "":
        plt.show()
    else:
        plt.savefig(path)


def plot_mean_std_dev_fitness_arrays(title: str, axis_title: str, fitness_charts: [], mean_std_dev_fit_values: [],
                                     path=""):
    fig, ax = plt.subplots()
    x = np.arange(0.0, len(fitness_charts[0]), 1.0)
    """
    Linestyles and colors are listed at matplotlib tutorials:
    
        https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html
    
    The following lists contain all values available for generating plots:
    
        * colors
        * markers (e. g. triangles on the lines)
        * styles (e. g. dots alligned on straight lines)     
    """
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown',
              'pink', 'gray', 'olive', 'cyan']
    markers = ['-', '--', ':', '.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D',
               'd', '|', '_']
    styles = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']

    i = 0
    for chart in fitness_charts:
        if len(chart) == len(x):
            # clr = colors[randrange(len(colors)-1)]
            ax.plot(x, chart, linestyle=styles[randrange(len(styles) - 1)], color='tab:gray',
                    label=str(i) + ": " + axis_title)
        i = i + 1

    ax.plot(x, [v[0] for v in mean_std_dev_fit_values], linestyle='-', color='tab:red', label="Mean")
    ax.plot(x, [v[0] + v[1] for v in mean_std_dev_fit_values], linestyle='-', color='tab:orange')
    ax.plot(x, [v[0] - v[1] for v in mean_std_dev_fit_values], linestyle='dotted', color='tab:orange')
    ax.fill_between(x, [v[0] + v[1] for v in mean_std_dev_fit_values], [v[0] - v[1] for v in mean_std_dev_fit_values],
                    alpha=0.2, color='tab:orange', label="StdDev")
    # if len(fitness_charts) > 1:
    #    ax.fill_between(x, fitness_charts[0], fitness_charts[-1], alpha=0.2, label="Range of Runs")
    #    ax.fill_between(x, fitness_charts[1], fitness_charts[-1], alpha=0.2, label="Range of Runs")
    # ax.plot(x, fit_avg, 'o', color='tab:brown')

    plt.grid(True)
    ax.set_title(title)
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    ax.set_ylim([0.0, 1.0])
    ax.legend()

    if path == "":
        plt.show()
    else:
        plt.savefig(path)


def fancy_mean_plot():
    Nsteps = 500
    t = np.arange(Nsteps)

    mu = 0.002
    sigma = 0.01

    # the steps and position
    S = mu + sigma * np.random.randn(Nsteps)
    X = S.cumsum()

    # the 1 sigma upper and lower analytic population bounds
    lower_bound = mu * t - sigma * np.sqrt(t)
    upper_bound = mu * t + sigma * np.sqrt(t)

    fig, ax = plt.subplots(1)
    ax.set_title("Fancy Plot")
    ax.plot(t, X, lw=2, label='walker position')
    ax.plot(t, mu * t, lw=1, label='population mean', color='C0', ls='--')
    ax.fill_between(t, lower_bound, upper_bound, facecolor='C0', alpha=0.4,
                    label='1 sigma range')
    ax.legend(loc='upper left')

    # here we use the where argument to only fill the region where the
    # walker is above the population 1 sigma boundary
    ax.fill_between(t, upper_bound, X, where=X > upper_bound, fc='red', alpha=0.4)
    ax.fill_between(t, lower_bound, X, where=X < lower_bound, fc='red', alpha=0.4)
    ax.set_xlabel('num steps')
    ax.set_ylabel('position')
    ax.grid()
    fig.show()


def entropy_fitness_plot():
    Nsteps = 10
    t = np.arange(Nsteps)

    # the steps and position
    S = -1.0 * np.log(0.5 * t) + 2
    X = np.log(0.5 * t) + 0.5

    fig, ax = plt.subplots(1)
    ax.set_title("Entropy Fitness Relation")

    ax.plot(t, S, lw=2, label='fitness')
    ax.plot(t, X, lw=1, label='entropy')
    ax.fill_between(t, S, X, facecolor='C0', alpha=0.4,
                    label='overlap')
    ax.legend(loc='upper left')

    ax.set_xlabel('scenarios')
    ax.set_ylabel('fitness / entropy')
    ax.grid()
    fig.show()


def fitness_boxplots():
    # Random test data
    np.random.seed(19680801)
    all_data = [np.random.normal(0, std, size=100) for std in range(1, 4)]
    labels = ['x1', 'x2', 'x3']

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

    # rectangular box plot
    bplot1 = ax1.boxplot(all_data,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
    ax1.set_title('Rectangular box plot')

    # notch shape box plot
    bplot2 = ax2.boxplot(all_data,
                         notch=True,  # notch shape
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
    ax2.set_title('Notched box plot')

    # fill with colors
    colors = ['pink', 'lightblue', 'lightgreen']
    for bplot in (bplot1, bplot2):
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)

    # adding horizontal grid lines
    for ax in [ax1, ax2]:
        ax.yaxis.grid(True)
        ax.set_xlabel('Three separate samples')
        ax.set_ylabel('Observed values')

    plt.show()


def computations_per_computing_unit():
    labels = ['Carbon Fibers', 'Stitched Fibers', 'Pultrusion Resin', 'MVTec Anomaly', 'Steel Welding']
    fpga_means = [20, 35, 30, 35, 27]
    cpu_means = [25, 32, 34, 20, 25]
    fpga_std = [2, 3, 4, 1, 2]
    cpu_std = [3, 5, 2, 3, 3]
    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, fpga_means, width, yerr=fpga_std, label='FPGA')
    ax.bar(labels, cpu_means, width, yerr=cpu_std, bottom=fpga_means,
           label='CPU')

    ax.set_ylabel('Percentage')
    ax.set_title('Percentage of operations by computing unit')
    ax.legend()

    plt.show()
