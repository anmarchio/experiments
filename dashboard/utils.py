import json
import os
import statistics

import numpy as np

from api import env_var
from api.database import Database
from api.models import Dataset
from dashboard.vars import PATH_TO_DATASET_NAME_MAP


def get_mean_fitness_per_dataset(norm_arr_dict: {}, m_idx):
    db = Database()
    print("DB path: " + env_var.SQLITE_PATH)
    list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session())

    mean_fitness_and_complexity_per_dataset = {}

    #for k in list_of_runs_fitness.keys():
    #    # Get key for the dataset to source mapping
    #    try:
    #        print("Name for " + list_of_runs_fitness[k]['source'] + " is: " + PATH_TO_DATASET_NAME_MAP[list_of_runs_fitness[k]['source']])
    #    except:
    #        print("[ERROR] no key for " + list_of_runs_fitness[k]['source'])

    for k in list_of_runs_fitness.keys():
        # Get key for the dataset to source mapping
        dataset_name = PATH_TO_DATASET_NAME_MAP[list_of_runs_fitness[k]['source']]

        # Get number of images contained in dataset
        number_of_images = list_of_runs_fitness[k]['number_of_images']

        # Get mean and stdv
        fitness_mean, fitness_stddev = compute_best_mean_and_std_dev(list_of_runs_fitness, k)
        complexity_mean = 0.0
        if dataset_name is not None and len(norm_arr_dict[dataset_name]) > 0:
            values = []
            for img in norm_arr_dict[dataset_name]:
                if m_idx < len(img):
                    values.append(img[m_idx])
            # complexity_mean = np.mean([img[m_idx] for img in norm_arr_dict[dataset_name]])
            complexity_mean = np.mean(values)

            # Check if key is already in dict
        if dataset_name in mean_fitness_and_complexity_per_dataset.keys():
            mean_fitness_and_complexity_per_dataset[dataset_name][0].append(fitness_mean)
            mean_fitness_and_complexity_per_dataset[dataset_name][1].append(complexity_mean)
        else:
            mean_fitness_and_complexity_per_dataset[dataset_name] = [[fitness_mean], [complexity_mean],
                                                                     number_of_images]

    return mean_fitness_and_complexity_per_dataset


def print_fitness_values_in_table(dataset_names: [], mean_std_dev_fit_per_dataset: []):
    print("| ID ", "| Dataset ", "| Mean", "| Std Dev |")
    if np.array(mean_std_dev_fit_per_dataset)[:, 0].size != \
            np.array(mean_std_dev_fit_per_dataset)[:, 1].size != \
            len(dataset_names):
        print("[ERROR] Array Mismatch")
    for i in range(np.array(mean_std_dev_fit_per_dataset)[:, 0].size):
        # [:, 0] = mean
        # [:, 1] = std dev
        ds_id = dataset_names[i][0]
        name = dataset_names[i][1]
        print(
            "| " + ds_id,
            " | " + name,
            " | " + str(round(np.array(mean_std_dev_fit_per_dataset)[:, 0][i], 3)) +
            " | " + str(round(np.array(mean_std_dev_fit_per_dataset)[:, 1][i], 3)) +
            " |"
        )


def extract_dataset_name(name, source, idxs: []):
    """
    Extracts the name of a dataset from within a system path
    and removes all irrelevant characters or non-dataset related labels.
    """
    print("source: ", source)
    split_path = source.split(os.sep)
    run_ids = ""
    for idx in idxs:
        run_ids = str(idx) + ","
    if name not in ['unknown', 'train', 'train"', 'train_cgp', 'train_cgp"',  'training']:
        fig_title = name
    elif len(split_path) > 1:
        fig_title = split_path[-2] + split_path[-1]
    else:
        fig_title = split_path[-1]
    fig_title = fig_title.replace('_training', '')
    fig_title = fig_title.replace('_train', '')
    fig_title = fig_title.replace('/training', '')
    fig_title = fig_title.replace('train', '')
    fig_title = fig_title.replace('train_cgp', '')
    fig_title = fig_title.replace('_cgp', '')
    fig_title = fig_title.replace('_large', '_lg')
    fig_title = fig_title.replace('_small', '_sm')
    fig_title = fig_title.replace('\"', '')
    return run_ids, fig_title


def compute_mean_and_std_dev(fit_values):
    mean_std_dev_fit_values = []
    for i in range(len(fit_values[0])):
        values = [chrt[i] for chrt in fit_values]
        if len(values) > 1:
            mean_std_dev_fit_values.append([statistics.mean(values), statistics.stdev(values)])
        else:
            mean_std_dev_fit_values.append([values[0], 0.0])
    return mean_std_dev_fit_values


def compute_best_mean_and_std_dev(values: []):
    best_fit_values = [v[-1].best_individual_fitness for v in values]

    if len(best_fit_values) > 1:
        return [statistics.mean(best_fit_values), statistics.stdev(best_fit_values)]
    elif len(best_fit_values) == 0:
        return [0.0, 0.0]
    return [best_fit_values[0], 0.0]


def data_linking(list_of_runs_fitness):
    linked_list = {}
    for k in list_of_runs_fitness.keys():
        source = list_of_runs_fitness[k]['source'].replace('"', '')
        source = source.replace(' ', '')
        dataset_name = PATH_TO_DATASET_NAME_MAP[source]

        if dataset_name in linked_list.keys():
            linked_list[dataset_name].append(list_of_runs_fitness[k])
        else:
            linked_list[dataset_name] = [list_of_runs_fitness[k]]

    return linked_list


def mean_std_dev_fitness_per_dataset(list_of_runs_fitness):
    linked_list_of_runs_fitness = data_linking(list_of_runs_fitness)

    dataset_names = []
    mean_std_dev_fit_per_dataset = []
    number_of_images = []

    for k in linked_list_of_runs_fitness.keys():
        values = []
        indices = []

        for rf in linked_list_of_runs_fitness[k]:
            if len(rf["values"]) > 0:
                values += rf["values"]
                indices.append(rf["id"])
                print("ID: ", str(rf["id"]), ", reading ...")
            else:
                print("ID: ", str(rf["id"]), ", [EMPTY]")
                continue

        if len(values) > 0:
            # only add values to list if not empty
            mean_std_dev_fit_per_dataset.append(compute_best_mean_and_std_dev(values))

            ids, name = extract_dataset_name(linked_list_of_runs_fitness[k][0]["name"], linked_list_of_runs_fitness[k][0]["source"], indices)
            dataset_names.append([ids, name])

            number_of_images.append(linked_list_of_runs_fitness[k][0]["number_of_images"])

    return dataset_names, mean_std_dev_fit_per_dataset, number_of_images


def read_file_and_return_norm_dict(file_name: str) -> {}:
    f = open(file_name, 'r')
    norm_arr_dict_list = json.load(f)
    f.close()
    return norm_arr_dict_list
