import json
import os
import statistics

from api import env_var
from api.database import Database
from api.models import Dataset


def get_mean_fitness_per_dataset(dataset_names):
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)
    list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session())
    mean_fitness_per_dataset = {}

    source_names=[]
    for k in list_of_runs_fitness.keys():
        source_names.append(list_of_runs_fitness[k]['source'])
    return source_names
    for k in list_of_runs_fitness.keys():
        for name in dataset_names:
            index = list_of_runs_fitness[k]['source'].find(name)
            if index > -1:
                # extract best fitness for dataset
                mean, stddev = compute_best_mean_and_std_dev(list_of_runs_fitness, k)
                if name in mean_fitness_per_dataset:
                    mean_fitness_per_dataset[name].append(mean)
                else:
                    mean_fitness_per_dataset[name] = [mean]
    return mean_fitness_per_dataset


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


def compute_mean_and_std_dev(fit_values):
    mean_std_dev_fit_values = []
    for i in range(len(fit_values[0])):
        values = [chrt[i] for chrt in fit_values]
        if len(values) > 1:
            mean_std_dev_fit_values.append([statistics.mean(values), statistics.stdev(values)])
        else:
            mean_std_dev_fit_values.append([values[0], 0.0])
    return mean_std_dev_fit_values


def compute_best_mean_and_std_dev(list_of_runs_fitness, k):
    best_fit_values = [v[-1].best_individual_fitness for v in list_of_runs_fitness[k]["values"]]

    if len(best_fit_values) > 1:
        return [statistics.mean(best_fit_values), statistics.stdev(best_fit_values)]
    elif len(best_fit_values) == 0:
        return [0.0, 0.0]
    return [best_fit_values[0], 0.0]


def mean_std_dev_fitness_per_dataset(list_of_runs_fitness):
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
    return dataset_names, mean_std_dev_fit_per_dataset


def read_file_and_return_norm_dict(file_name: str) -> {}:
    f = open(file_name, 'r')
    norm_arr_dict_list = json.load(f)
    f.close()
    return norm_arr_dict_list
