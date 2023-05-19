import json
import os
from datetime import datetime

import numpy as np

from api import env_var
from api.database import Database
from api.models import Dataset
from dashboard.plotting import plot_mean_std_dev_fitness_arrays, plot_fitness_per_dataset, create_scatterplot, \
    create_complexity_plot
from dashboard.utils import read_file_and_return_norm_dict, mean_std_dev_fitness_per_dataset, compute_mean_and_std_dev, \
    extract_dataset_name, get_mean_fitness_per_dataset, print_fitness_values_in_table, data_linking
from dashboard.vars import COMPLEXITY_METRICS


def compute_complexity_and_fitness_correlation(json_file_path):
    """
    Plot of Correlation of Complexity and CGP Fitness per metric
    """
    # normalize values computed from images to [0,1]
    norm_arr_dict = read_file_and_return_norm_dict(json_file_path)
    # create txt file for values before plotting
    pearson_rs = {}
    f = open(os.path.join("out", "plots", datetime.now().strftime('%Y%m%d-%H%M%S') + "_metrics.txt"), "w")
    for i in range(len(COMPLEXITY_METRICS)):
        mean_fitness_and_complexity_per_dataset = get_mean_fitness_per_dataset(norm_arr_dict, i)

        f.write("Metric: " + COMPLEXITY_METRICS[i] + "\n")
        print("Metric: " + COMPLEXITY_METRICS[i])

        f.write("| Dataset    | Avg. Fit. | Entropy | # Images |\n")
        print("| Dataset    | Avg. Fit. | Entropy | # Images |")
        for k in mean_fitness_and_complexity_per_dataset:
            mean_fitness = np.nanmean(mean_fitness_and_complexity_per_dataset[k][0])
            mean_complexity = np.nanmean(mean_fitness_and_complexity_per_dataset[k][1])
            number_of_images = mean_fitness_and_complexity_per_dataset[k][2]
            if k is None:
                k = 'None'
            if mean_fitness is None:
                mean_fitness = 0.0
            if mean_complexity is None:
                mean_complexity = 0.0
            print("| " + k + " | " + str(mean_fitness) + " | " + str(mean_complexity) + " | " + str(
                number_of_images) + " |")
            f.write("| " + k + " | " + str(mean_fitness) + " | " + str(mean_complexity) + " | " + str(
                number_of_images) + " |\n")

        # get Pearson's r
        fit_arr = [mean_fitness_and_complexity_per_dataset[k][0][0] for k in mean_fitness_and_complexity_per_dataset]
        comp_arr = [mean_fitness_and_complexity_per_dataset[k][1][0] for k in mean_fitness_and_complexity_per_dataset]
        r = np.corrcoef(fit_arr, comp_arr)
        correlation = r[0, 1]
        pearson_rs[COMPLEXITY_METRICS[i]] = correlation
        print("\nCorrelation for " + COMPLEXITY_METRICS[i] + ": " + str(correlation))

        create_complexity_plot(
            "Complexity per Dataset",
            COMPLEXITY_METRICS[i],
            list(mean_fitness_and_complexity_per_dataset.keys()),
            comp_arr,
            path=os.path.join("out", "plots",
                              datetime.now().strftime('%Y%m%d-%H%M%S') +
                              COMPLEXITY_METRICS[i] + "_bplot.png")
        )

        create_scatterplot(
            COMPLEXITY_METRICS[i],
            fit_arr,
            comp_arr,
            save_to=os.path.join("out", "plots",
                                 datetime.now().strftime('%Y%m%d-%H%M%S') +
                                 COMPLEXITY_METRICS[i] + "_scatterplot.png")
        )
        f.write("----------------------------------------------------------------\n\n")

    f.write("| Metric | Cor(fit, v) |\n")
    for p in pearson_rs:
        print("| " + p + " | " + str(pearson_rs[p]) + "|\n")
        f.write("| " + p + " | " + str(pearson_rs[p]) + "|\n")
    f.close()


def read_fitness_values(paths: dict(), filename: str, identifier: str):
    fitness_arr = []
    if os.path.exists(paths[filename]):
        with open(paths[filename]) as fitness_file:
            fitness_data = json.load(fitness_file)
            for val in fitness_data:
                fitness_arr.append(float(val[identifier]))
    return fitness_arr


def generate_plots_from_json(source_path, target_path):
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
        for dir in os.listdir(analyzer_dir):
            paths = {
                'source': os.path.join(source_path, batch_name, "source.json"),
                'AvgOffspringFit': os.path.join(source_path, batch_name, "Analyzer", dir, "AvgOffspringFit.json"),
                'AvgPopulationFit': os.path.join(source_path, batch_name, "Analyzer", dir, "AvgPopulationFit.json"),
                'BestIndividualFit': os.path.join(source_path, batch_name, "Analyzer", dir, "BestIndividualFit.json")
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
        plot_mean_std_dev_fitness_arrays(
            title=title,
            axis_title="Offspring Mean",
            fitness_charts=avg_off_fit,
            mean_std_dev_fit_values=[],
            path=''
        )
        plot_mean_std_dev_fitness_arrays(
            title=title,
            axis_title="Population Mean",
            fitness_charts=avg_pop_fit,
            mean_std_dev_fit_values=[],
            path=''
        )
        plot_mean_std_dev_fitness_arrays(
            title=title,
            axis_title="Best Individual Mean",
            fitness_charts=best_ind_fit,
            mean_std_dev_fit_values=[],
            path=''
        )


def read_database_and_show_plots(min_generations, max_generations, grouped_dataset=False, show_legend=False):
    """
    Reads fitness evolution per dataset for all runs
    and write it to plots showing their mean and std dev per generation
    """
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)
    list_of_runs_fitness = {}

    if grouped_dataset:
        list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session(), min_generations,
                                                                           max_generations)
    else:
        list_of_runs_fitness = Dataset.get_runs_fitness_by_each_dataset(db.get_session())

    linked_list_of_runs_fitness = data_linking(list_of_runs_fitness)

    cnt = 0
    for k in linked_list_of_runs_fitness.keys():
        run_ids = [d['id'] for d in linked_list_of_runs_fitness[k]]
        if len(linked_list_of_runs_fitness[k]) > 0:
            print("ID: ", str(run_ids), ", reading ...")
        else:
            print("ID: ", str(run_ids), ", [EMPTY]")
            continue
        cnt += 1
        fit_values = []
        for d in linked_list_of_runs_fitness[k]:
            for r in d["values"]:
                fit_values.append([f.best_individual_fitness for f in r])

        if len(fit_values) > 0:
            mean_std_dev_fit_values = compute_mean_and_std_dev(fit_values)
            if show_legend:
                dataset_name = str(run_ids) + ", " + k
            plot_mean_std_dev_fitness_arrays(
                k,
                "Best Individual",
                fit_values,
                mean_std_dev_fit_values,
                path=os.path.join("scripts", "report", str(k) + ".png"),
                show_legend=show_legend
            )
    """
    # DEPRECATED
    # ----------
    cnt = 0
    for k in list_of_runs_fitness.keys():
        id = list_of_runs_fitness[k]["id"]
        if len(list_of_runs_fitness[k]["values"]) > 0:
            print("ID: ", id, ", reading ...")
        else:
            print("ID: ", id, ", [EMPTY]")
            continue
        cnt += 1
        fit_values = []
        for r in list_of_runs_fitness[k]["values"]:
            fit_values.append([f.best_individual_fitness for f in r])

        mean_std_dev_fit_values = compute_mean_and_std_dev(fit_values)

        if len(list_of_runs_fitness[k]["values"]) > 0:
            run_id, dataset_name = extract_dataset_name(list_of_runs_fitness[k]['name'], list_of_runs_fitness[k]['source'], [list_of_runs_fitness[k]['id']])
            if show_legend:
                dataset_name = str(run_id) + ", " + dataset_name
            plot_mean_std_dev_fitness_arrays(
                dataset_name,
                "Best Individual",
                fit_values,
                mean_std_dev_fit_values,
                path=os.path.join("scripts", "report", str(k) + ".png"),
                show_legend=show_legend
            )
    """


def read_database_and_plot_fitness_per_dataset(min_generations: int = 0, max_generations: int = None, show_names=False):
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)

    list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session(), min_generations,
                                                                       max_generations)
    dataset_names, mean_std_dev_fit_per_dataset, number_of_images, number_of_runs = mean_std_dev_fitness_per_dataset(list_of_runs_fitness)

    plot_fitness_per_dataset(
        "Fitness per Dataset",
        "Fitness",
        dataset_names,
        mean_std_dev_fit_per_dataset,
        orientation='v',
        path=os.path.join("scripts", "report", "fitness_per_dataset.png"),
        show_names=show_names
    )

    print_fitness_values_in_table(dataset_names, mean_std_dev_fit_per_dataset, number_of_images, number_of_runs)
