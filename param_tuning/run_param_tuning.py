import os
import sys

from api import env_var
from api.database import Database
from api.models import Dataset
from param_tuning.data_parser import extract_fitness_values, get_cgp_ls_sa_dict_from_pipelines
from param_tuning.dataset_pipeline_analysis import get_grouped_datasets_with_digraph_by_mean_fitness, \
    read_db_and_apply_algorithms_to_hdev, objective
from param_tuning.hdev_manual_mean.run_hdev_manual import MANUAL_HDEV_PIPELINES_MEAN
from param_tuning.local_search import run_local_search
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import write_digraph_to_files, \
    check_dir_exists, plot_bar_charts, results_to_latex_table
from settings import PARAM_TUNING_RESULTS_PATH, HDEV_RESULTS_PATH


def show_param_tuning_menu():
    print("\n")
    print("-" * 35)
    print("FOLLOW UP OPTIMIZATION using SA /LS")
    print("-" * 35)
    print("1 -- MANUAL 1: Export digraphs to txt")
    print("2 -- MANUAL 2: Read manual HDEV files and perform SA/LS")
    print("3 -- AUTOMATIC: Read DB and apply HDEV optimization")
    print("4 -- Plot results in bar charts")
    print("0 -- EXIT")

    print("\n")
    selection = input("Selection: ")
    try:
        if 0 < int(selection) < 5:
            return int(selection)
    except:
        selection = 0
    return 0


def selection_export_digraphs_to_txt(linked_list_of_mean_fitness_and_digraph):
    """
    1 -- MANUAL v1: Export digraphs to txt
    """
    # output folder for digraphs
    digraph_path = os.path.join(PARAM_TUNING_RESULTS_PATH, "digraphs")
    check_dir_exists(PARAM_TUNING_RESULTS_PATH)
    check_dir_exists(digraph_path)

    for ds_key in linked_list_of_mean_fitness_and_digraph.keys():
        dataset_digraph = linked_list_of_mean_fitness_and_digraph[ds_key]

        # Write dataset metadata and digraph to file in folder
        write_digraph_to_files(ds_key, dataset_digraph, digraph_path)


def selection_read_manual_hdev_files_and_perform_sa_ls():
    """
    2 -- MANUAL v2: Read manual HDEV files and perform SA/LS
    """
    manual_hdev_path = os.path.join(PARAM_TUNING_RESULTS_PATH, "manual_hdev")
    check_dir_exists(PARAM_TUNING_RESULTS_PATH)
    check_dir_exists(manual_hdev_path)

    for pipeline_name in MANUAL_HDEV_PIPELINES_MEAN:
        # Run simulated annealing on dataset
        run_simulated_annealing(pipeline_name, None, objective, True)

        # Then run local search
        run_local_search(pipeline_name, None, objective, True)


def selection_read_db_and_apply_hdev_optimization(db):
    print("!!! ATTENTION: This part has not been tested properly !!!")

    print("Do you want to continue? y/n")
    print("\n")
    yesno = input("Selection: ")
    if yesno == "y":
        experiment_datasets = Dataset.get_pipeline_by_each_dataset(db.get_session())

        read_db_and_apply_algorithms_to_hdev(experiment_datasets)
    else:
        print("Aborted.")


def selection_plot_cgp_results_in_bar_chart(linked_list_of_mean_fitness_and_digraph):
    print("Plot results in bar chart.")
    file_paths = [os.path.join(HDEV_RESULTS_PATH, "param_tuning", "manual_hdev", name + ".txt") for name in
                  MANUAL_HDEV_PIPELINES_MEAN]
    ls_results, sa_results = extract_fitness_values(file_paths)
    datasets = [name.replace("_mean_pipeline", "") for name in MANUAL_HDEV_PIPELINES_MEAN]

    cgp_results = get_cgp_ls_sa_dict_from_pipelines(datasets,
                                                    linked_list_of_mean_fitness_and_digraph,
                                                    ls_results,
                                                    sa_results)

    # datasets, cgp_results, ls_results, sa_results
    datasets.reverse()
    cgp_results.reverse()
    ls_results.reverse()
    sa_results.reverse()
    plot_bar_charts(datasets, cgp_results, ls_results, sa_results)

    datasets.reverse()
    cgp_results.reverse()
    ls_results.reverse()
    sa_results.reverse()
    print(results_to_latex_table(datasets, cgp_results, ls_results, sa_results))


def run_param_tuning() -> int:
    selection = show_param_tuning_menu()

    # Exit program
    if selection == 0:
        print("Exiting ...")
        return 0

    # Get database object from api.database
    db = Database()

    # Get linked list of grouped Datasets with according digraph closest to MEAN fitness
    linked_list_of_mean_fitness_and_digraph = {}

    if selection == 1 or selection >= 3:
        print("Get linked list of grouped Datasets with according digraph closest to MEAN fitness")
        print("-- from DB path: " + env_var.SQLITE_PATH)
        linked_list_of_mean_fitness_and_digraph = get_grouped_datasets_with_digraph_by_mean_fitness(db.get_session())

    # 1 -- MANUAL v1: Export digraphs to txt
    if selection == 1:
        selection_export_digraphs_to_txt(linked_list_of_mean_fitness_and_digraph)

    # 2 -- MANUAL v2: Read manual HDEV files and perform SA/LS
    if selection == 2:
        selection_read_manual_hdev_files_and_perform_sa_ls()

    # 3 -- AUTOMATIC: Read DB and apply HDEV optimization
    if selection == 3:
        # !!! ATTENTION: This part has not been tested properly !!!
        selection_read_db_and_apply_hdev_optimization(db)

    if selection == 4:
        selection_plot_cgp_results_in_bar_chart(linked_list_of_mean_fitness_and_digraph)

    return 0


if __name__ == '__main__':
    run_param_tuning()
    sys.exit()
