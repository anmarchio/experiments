import json
import os
import statistics
import sys
from datetime import datetime
from os.path import join as p_join

from api import env_var
from api.database import Database
from api.models import Dataset
from dashboard.utils import read_dir_to_norm_dict
from sample_plots import plot_sample, fancy_mean_plot, plot_fitness_evolution, \
    entropy_fitness_plot, fitness_boxplots, computations_per_computing_unit, plot_mean_std_dev_fitness_arrays, \
    plot_fitness_per_dataset


def compute_complexity_and_fitness_correlation(read_dir_path):
    norm_arr_dict = read_dir_to_norm_dict(read_dir_path)

    IMAGE_METRICS = [
        "Entropy",
         "Blurriness",
         "Brightness",
         "Img Size",
         "Lbl Size",
         "label_count_per_image",
         "relative_label_size",
         "hist_entropy",
         "jpeg_complexity",
         "fractal_dimension",
         "texture_features",
         "edge_density",
         "laplacian_variance",
         "num_superpixels"
    ]

    for metric in IMAGE_METRICS:
        create_boxplot(
            norm_arr_dict[metric],
            save_to=os.path.join(os.path.pardir, "out", datetime.strptime(datetime.utcnow(), '%Y%m%d-%H%M%S') + metric + '_bplot.png')
        )

        correlation = get_correlation(norm_arr_dict[metric])

        create_scatterplot(
            norm_arr_dict[metric],
            save_to=os.path.join(os.path.pardir, "out", datetime.strptime(datetime.utcnow(), '%Y%m%d-%H%M%S') + metric + '_scatterplot.png')
        )


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


def show_sample_plots():
    # Echo the input arguments to standard output
    print("Create sample plots ...")
    plot_sample()
    fancy_mean_plot()
    plot_fitness_evolution()
    entropy_fitness_plot()
    fitness_boxplots()
    computations_per_computing_unit()


def compute_mean_and_std_dev(fit_values):
    mean_std_dev_fit_values = []
    for i in range(len(fit_values[0])):
        values = [chrt[i] for chrt in fit_values]
        if len(values) > 1:
            mean_std_dev_fit_values.append([statistics.mean(values), statistics.stdev(values)])
        else:
            mean_std_dev_fit_values.append([values[0], 0.0])
    return mean_std_dev_fit_values


def extract_dataset_name(list_of_runs_fitness, k):
    print("source: ", os.path.split(list_of_runs_fitness[k]["source"])[-1])
    split_path = os.path.split(list_of_runs_fitness[k]["source"])
    if list_of_runs_fitness[k]["name"] not in ["unknown", "train", "train_cgp", "training"]:
        fig_title = str(id) + ", " + list_of_runs_fitness[k]["name"]
    elif len(split_path) > 1:
        fig_title = str(id) + ", " + split_path[-2] + split_path[-1]
    else:
        fig_title = str(id) + ", " + split_path[-1]
    return fig_title


def read_database_and_show_plots(grouped_dataset=False):
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)
    list_of_runs_fitness = {}

    if grouped_dataset:
        list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session())
    else:
        list_of_runs_fitness = Dataset.get_runs_fitness_by_each_dataset(db.get_session())

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
            dataset_name = extract_dataset_name(list_of_runs_fitness, k)

            plot_mean_std_dev_fitness_arrays(
                dataset_name,
                "Best Individual",
                fit_values,
                mean_std_dev_fit_values,
                path=p_join(os.path.curdir, '../scripts/report/' + str(k) + '.png')
            )


def compute_best_mean_and_std_dev(list_of_runs_fitness, k):
    best_fit_values = [v[-1].best_individual_fitness for v in list_of_runs_fitness[k]["values"]]

    if len(best_fit_values) > 1:
        return [statistics.mean(best_fit_values), statistics.stdev(best_fit_values)]
    return [best_fit_values[0], 0.0]


def read_database_and_plot_fitness_per_dataset():
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)

    list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session())
    dataset_names = []
    mean_std_dev_fit_per_dataset = []

    for k in list_of_runs_fitness.keys():
        id = list_of_runs_fitness[k]["id"]
        if len(list_of_runs_fitness[k]["values"]) > 0:
            print("ID: ", id, ", reading ...")
        else:
            print("ID: ", id, ", [EMPTY]")
            continue

        mean_std_dev_fit_per_dataset.append(compute_best_mean_and_std_dev(list_of_runs_fitness, k))

        if len(list_of_runs_fitness[k]["values"]) > 0:
            dataset_names.append(extract_dataset_name(list_of_runs_fitness, k))

    plot_fitness_per_dataset(
        "Fitness per Dataset",
        "Fitness",
        dataset_names,
        mean_std_dev_fit_per_dataset,
        path=p_join(os.path.curdir, '../scripts/report/fitness_per_dataset.png')
    )


def main() -> int:
    results_path = p_join(os.path.curdir, '../scripts/results')
    report_path = p_join(os.path.curdir, '../scripts/report')

    # show_sample_plots()
    # os.makedirs(report_path, mode=777, exist_ok=True)

    read_database_and_plot_fitness_per_dataset()

    yesno = input('Continue read_database_and_show_plots? (y/n)')

    if yesno == "y":
        read_database_and_show_plots(grouped_dataset=True)

    # Creates HTML file report/index.html
    # if SPECIFIC_SOURCE_PATH is not "":
    #  generate_plots_from_json(SPECIFIC_SOURCE_PATH, report_path)
    # else:
    #  generate_plots_from_json(results_path, report_path)

    return 0


if __name__ == '__main__':
    main()
    # next section explains the use of sys.exit
    sys.exit()
