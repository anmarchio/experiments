import os
import sys

from os.path import join as p_join

from dashboard.create_analysis_plots import read_database_and_plot_fitness_per_dataset, read_database_and_show_plots, \
    generate_plots_from_json, compute_complexity_and_fitness_correlation
from dashboard.dashboard import matplot_dashboard, hvplot_test
from dashboard.plotting import computations_per_computing_unit, plot_sample, plot_fitness_evolution, \
    fancy_mean_plot, entropy_fitness_plot, fitness_boxplots

# SPECIFIC_SOURCE_PATH = os.path.join("P:\\", "99 Austausch_TVöD", "mara", "Dissertation", "20230120results_dl2")
from dashboard.utils import clean_up_dataset_metadata
from dashboard.vars import PATH_TO_DATASET_NAME_MAP

SPECIFIC_SOURCE_PATH = ""
# SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230329-163243data_arr.json")
SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230509-025213data_arr.json")


def show_program_menu():
    print('1 - Plot complexity and fitness for evias datasets')
    print('2 - Read DB and show plot with ALL FITNESS values')
    print('3 - Read DB and show plots')
    print('4 - Generate HTML reports')
    print('5 - Print Dashboard Plots')
    print('6 - Print Sample Plots')
    print('7 - Clean Up Dataset Metadata')
    print('0 - EXIT')
    selection = input('Selection: ')
    if 0 < int(selection) < 7:
        return int(selection)
    return 0


def main() -> int:
    """
    Set Default Paths
    """
    results_path = p_join(os.path.curdir, '../scripts/results')
    report_path = p_join(os.path.curdir, '../scripts/report')

    if not os.path.exists(report_path):
        os.makedirs(report_path, mode=777, exist_ok=True)

    selection = show_program_menu()
    if selection == 0:
        return 0

    # yesno = input('Plot complexity and fitness? (y/n)')
    if selection == 1 and SAMPLE_IMAGES_DIR_PATH != "":
        compute_complexity_and_fitness_correlation(SAMPLE_IMAGES_DIR_PATH)

    # yesno = input('Read DB and show plot with ALL FITNESS? (y/n)')
    if selection == 2:
        read_database_and_plot_fitness_per_dataset(140, 500)

    # yesno = input('read_database_and_show_plots? (y/n)')
    if selection == 3:
        read_database_and_show_plots(grouped_dataset=True)

    # yesno = input('Generate HTML reports? (y/n)')
    if selection == 4:
        # Creates HTML file report/index.html
        if SPECIFIC_SOURCE_PATH != "":
            generate_plots_from_json(SPECIFIC_SOURCE_PATH, report_path)
        else:
            generate_plots_from_json(results_path, report_path)

    """
    Dashboard Samples
    """
    # yesno = input("Print Dashboard Plots (y/n):")
    if selection == 5:
        matplot_dashboard()
        hvplot_test()
    """
    Sample Plots
    """
    # yesno = input("Print Sample Plots (y/n):")
    if selection == 6:
        plot_sample()
        plot_fitness_evolution()
        fancy_mean_plot()
        entropy_fitness_plot()
        fitness_boxplots()
        computations_per_computing_unit()

    """
    Clean Up Dataset Metadata
    * shorten descriptions to one name without the system path
    * group datasets that belong to one
    """
    if selection == 7:
        clean_up_dataset_metadata()
    return 0


if __name__ == '__main__':
    main()
    # next section explains the use of sys.exit
    sys.exit()
