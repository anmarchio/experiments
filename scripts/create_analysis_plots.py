import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from os.path import join as p_join
from matplotlib.patches import Polygon

SPECIFIC_SOURCE_PATH = os.path.join("P:\\","99 Austausch_TVöD","mara","Dissertation","20230120results_dl2")

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


def plot_fitness_arrays(title: str, fitness_charts: []):

    fig, ax = plt.subplots()
    x = np.arange(0.0, len(fitness_charts[0]), 1.0)
    colors = ['red', 'orange', 'brown', 'green', 'gray']
    styles = ['-', '--', ':']
    i = 0
    for chart in fitness_charts:
        if len(chart) == len(x):
            linestyle = styles[i]
            clr = colors[i]
            ax.plot(x, chart, linestyle, color='tab:' + clr, label=str(i) + ": Offsprg Mean Fit")
        i += 1
    # ax.fill_between(x, fit_max, fit_min, alpha=0.2, label="Min/Max Range")

    # ax.plot(x, fit_avg, 'o', color='tab:brown')
    plt.grid(True)
    ax.set_title(title)
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    ax.legend()

    plt.show()


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


def read_fitness_values(paths: dict(), filename: str, identifier: str):
    fitness_arr = []
    if os.path.exists(paths[filename]):
        with open(paths[filename]) as fitness_file:
            fitness_data = json.load(fitness_file)
            for val in fitness_data:
                fitness_arr.append(float(val[identifier]))
    return fitness_arr


def generate_plots(source_path, target_path):
    # data[0]['Generation']
    # data[0]['AverageOffspringFitness']
    # src_data[0]['trainingDataDirectory']
    for batch_name in os.listdir(source_path):
        title = "undefined"
        avg_off_fit = []
        avg_pop_fit = []
        best_ind_fit = []
        analyzer_dir = os.path.join(source_path, batch_name, "Analyzer")

        if not os.path.exists(analyzer_dir):
            continue
        i = 0
        for iteration in os.listdir(analyzer_dir):
            paths = {
                'source': os.path.join(source_path, batch_name, "source.json"),
                'AvgOffspringFit': os.path.join(source_path, batch_name, "Analyzer", str(i), "AvgOffspringFit.json"),
                'AvgPopulationFit': os.path.join(source_path, batch_name, "Analyzer", str(i), "AvgPopulationFit.json"),
                'BestIndividualFit': os.path.join(source_path, batch_name, "Analyzer", str(i), "BestIndividualFit.json")
            }

            # title from source.json
            if os.path.exists(paths['source']):
                with open(paths['source']) as sf:
                    src_data = json.load(sf)
                    title = src_data[0]['trainingDataDirectory']


            avg_off_fit.append(read_fitness_values(paths, 'AvgOffspringFit', 'AverageOffspringFitness'))
            avg_pop_fit.append(read_fitness_values(paths, 'AvgPopulationFit', 'AveragePopulationFitness'))
            best_ind_fit.append(read_fitness_values(paths, 'BestIndividualFit', 'BestIndividualFitness'))

            i += 1

        # BestIndividualFit.json
        plot_fitness_arrays(
            title,
            best_ind_fit
        )



def main() -> int:
    results_path = p_join(os.path.curdir, 'results')
    report_path = p_join(os.path.curdir, 'report')

    """Echo the input arguments to standard output"""
    print("Create sample plots ...")
    #plot_sample()
    #fancy_mean_plot()
    #plot_fitness_evolution()
    #entropy_fitness_plot()
    #fitness_boxplots()
    #computations_per_computing_unit()

    os.makedirs(report_path, mode=777, exist_ok=True)

    # Creates HTML file report/index.html
    if SPECIFIC_SOURCE_PATH:
        generate_plots(SPECIFIC_SOURCE_PATH, report_path)
    else:
        generate_plots(results_path, report_path)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
