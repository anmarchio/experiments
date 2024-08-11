import os

import numpy as np

from datetime import datetime
from param_tuning.hdev.hdev_template import HDEV_FUNCTIONS, HDEV_HEADER, HDEV_FOOTER, HDEV_TEMPLATE_CODE
from settings import HDEV_RESULT


def extract_bounds_from_graph(graph):
    bounds = np.array

    for k in graph['pipeline'].keys():
        if k in HDEV_FUNCTIONS.keys():
            i = 0
            for p in graph['pipeline'][k].keys():
                # graph['pipeline'][k][p]
                if np.size(bounds) > 1:
                    bounds = np.append(bounds, np.array([[0, 255]]), axis=0)
                else:
                    bounds = np.array([[0, 255]])
                i += 1

    return bounds


def write_to_file(results_path, algorithm, source, experiment_datetime, experiment_path, best_params, best_score):
    # def save_scores_to_db(scores: [], model_name: str, root_path: str, dataset_path: {}):
    # existing_results = load_results(RESULTS_DB_PATH)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_results = [
        {
            # "ID": str(len(existing_results)),
            "datetime": current_datetime,
            "algorithm": algorithm,
            "source": source,
            "experiment_datetime": experiment_datetime,
            "experiment_path": experiment_path,
            "best_params": best_params,
            "best_score": best_score
        }
    ]
    line = current_datetime + ";" + \
           algorithm + ";" + source + ";" + \
           experiment_datetime + ";" + \
           experiment_path + ";" + \
           best_params + ";" + \
           best_score + ";\n"
    # xisting_results.extend(new_results)
    # save_results(existing_results, RESULTS_DB_PATH)
    f = open(results_path, "a")
    f.write(line)
    f.close()


def print_tex(results_path):
    raise NotImplementedError


def translate_to_hdev(graph, params):
    # HDEV xml style header
    hdev_output = HDEV_HEADER

    # define source and output path for reading image and writing results (binary images)
    hdev_output += "<l>source_path := '" + graph['training_path'].replace("\\", "/") + "/images'</l>\n"

    hdev_output += "<l>output_path := '"
    hdev_output += get_pipeline_folder_name(graph['path']).replace("\\", "/") + "'</l>\n"

    hdev_output += HDEV_TEMPLATE_CODE

    # decode pipeline and translate to hdev code
    # node by node from graph dict
    for k in graph['pipeline'].keys():
        if k in HDEV_FUNCTIONS.keys():
            hdev_output += "<l>        " + \
                           HDEV_FUNCTIONS[k]['name'] + "(" + \
                           HDEV_FUNCTIONS[k]['in'] + ", " + \
                           HDEV_FUNCTIONS[k]['out'] + ", "
            i = 0
            for p in graph['pipeline'][k].keys():
                # Reading the CGP generated parameter
                # hdev_output += graph['pipeline'][k][p]
                # Instead, use the simulated annealing parametre
                hdev_output += str(params[i])
                i += 1
                if i < len(graph['pipeline'][k].keys()):
                    hdev_output += ", "

            hdev_output += ")</l>\n"

    # add the footer hdev code
    # to write results to binary image
    hdev_output += HDEV_FOOTER

    return hdev_output


def get_pipeline_folder_name(file_path):
    return HDEV_RESULT + os.path.sep + \
        file_path.split(os.path.sep)[-4] + "-" + \
        file_path.split(os.path.sep)[-3] + "-" + \
        file_path.split(os.path.sep)[-2]


def write_hdev_code_to_file(file_path: str, hdev_code: str) -> str:
    hdev_path = get_pipeline_folder_name(file_path) + ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path
