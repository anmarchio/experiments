import json
import os
import sys
from os.path import join as p_join

from api import env_var
from api.database import Database
from api.models import Dataset
from sample_plots import plot_fitness_arrays, plot_sample, fancy_mean_plot, plot_fitness_evolution, \
    entropy_fitness_plot, fitness_boxplots, computations_per_computing_unit

# SPECIFIC_SOURCE_PATH = os.path.join("P:\\", "99 Austausch_TVöD", "mara", "Dissertation", "20230120results_dl2")

SPECIFIC_SOURCE_PATH = ""


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

        plot_fitness_arrays(
            title,
            "Offspring Mean",
            avg_off_fit
        )
        plot_fitness_arrays(
            title,
            "Population Mean",
            avg_pop_fit
        )
        plot_fitness_arrays(
            title,
            "Best Individual Mean",
            best_ind_fit
        )


def show_sample_plots():
    # Echo the input arguments to standard output
    print("Create sample plots ...")
    plot_sample()
    fancy_mean_plot()
    plot_fitness_evolution()
    entropy_fitness_plot()
    fitness_boxplots()
    computations_per_computing_unit()


def read_database_and_show_plots():
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)
    list_of_runs_fitness = Dataset.get_runs_fitness_by_dataset(db.get_session())
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

        if list_of_runs_fitness[k]["source"] != "unknown":
            print("source: ", os.path.split(list_of_runs_fitness[k]["source"])[-1])
            split_path = os.path.split(list_of_runs_fitness[k]["source"])
            if list_of_runs_fitness[k]["name"] not in ["unknown", "train", "train_cgp", "training"]:
                fig_title = str(id) + ", " + list_of_runs_fitness[k]["name"]
            elif len(split_path) > 1:
                fig_title = str(id) + ", " +split_path[-2] + split_path[-1]
            else:
                fig_title = str(id) + ", " +split_path[-1]
            plot_fitness_arrays(
                fig_title,
                "Best Individual",
                fit_values
            )


def main() -> int:
    results_path = p_join(os.path.curdir, '../scripts/results')
    report_path = p_join(os.path.curdir, '../scripts/report')

    #show_sample_plots()
    # os.makedirs(report_path, mode=777, exist_ok=True)

    read_database_and_show_plots()

    # Creates HTML file report/index.html
    #if SPECIFIC_SOURCE_PATH is not "":
    #  generate_plots_from_json(SPECIFIC_SOURCE_PATH, report_path)
    #else:
    #  generate_plots_from_json(results_path, report_path)

    return 0


if __name__ == '__main__':
    main()
    # next section explains the use of sys.exit
    sys.exit()
