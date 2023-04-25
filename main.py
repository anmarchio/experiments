import os
import sys

from os.path import join as p_join

from dashboard.create_analysis_plots import read_database_and_plot_fitness_per_dataset, read_database_and_show_plots, \
    generate_plots_from_json, compute_complexity_and_fitness_correlation
from dashboard.dashboard import matplot_dashboard, hvplot_test
from dashboard.plotting import computations_per_computing_unit, plot_sample, plot_fitness_evolution, \
    fancy_mean_plot, entropy_fitness_plot, fitness_boxplots

# SPECIFIC_SOURCE_PATH = os.path.join("P:\\", "99 Austausch_TVöD", "mara", "Dissertation", "20230120results_dl2")
from dashboard.vars import PATH_TO_DATASET_NAME_MAP

SPECIFIC_SOURCE_PATH = ""
SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230329-163243data_arr.json")


def main():
    """
    Plots from Database
    """
    results_path = p_join(os.path.curdir, '../scripts/results')
    report_path = p_join(os.path.curdir, '../scripts/report')

    if not os.path.exists(report_path):
        os.makedirs(report_path, mode=777, exist_ok=True)

    yesno = input('Plot complexity and fitness? (y/n)')
    if yesno == "y" and SAMPLE_IMAGES_DIR_PATH != "":
        "|||||||||||||||||||||||||||||||||||||||||||||"
        "                     HERE                    "
        "|||||||||||||||||||||||||||||||||||||||||||||"
        "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
        compute_complexity_and_fitness_correlation(SAMPLE_IMAGES_DIR_PATH)

    yesno = input('Read DB and show plot with ALL FITNESS? (y/n)')
    if yesno == "y":
        read_database_and_plot_fitness_per_dataset()

    yesno = input('read_database_and_show_plots? (y/n)')
    if yesno == "y":
        read_database_and_show_plots(grouped_dataset=True)

    yesno = input('Generate HTML reports? (y/n)')
    if yesno == "y":
        # Creates HTML file report/index.html
        if SPECIFIC_SOURCE_PATH != "":
            generate_plots_from_json(SPECIFIC_SOURCE_PATH, report_path)
        else:
            generate_plots_from_json(results_path, report_path)

    """
    Dashboard Samples
    """
    yesno = input("Print Dashboard Plots (y/n):")
    if yesno == 'y':
        matplot_dashboard()
        hvplot_test()
    """
    Sample Plots
    """
    yesno = input("Print Sample Plots (y/n):")
    if yesno == 'y':
        plot_sample()
        plot_fitness_evolution()
        fancy_mean_plot()
        entropy_fitness_plot()
        fitness_boxplots()
        computations_per_computing_unit()

    return 0


if __name__ == '__main__':
    main()
    # next section explains the use of sys.exit
    sys.exit()
