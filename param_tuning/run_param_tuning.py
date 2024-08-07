import sys
import os

import numpy as np

from local_search import run_local_search
from param_tuning.hdev.hdev_template import hdev_header, hdev_footer, hdev_functions, hdev_folder
from simulated_annealing import run_simulated_annealing
from read_dot import read_dot_file, parse_dot

from os.path import join as p_join


def run_pipeline(amplitude, threshold_value):
    raise NotImplementedError


def objective(params):
    amplitude, threshold_value = params
    # Run the pipeline with given parameters and evaluate performance
    # Assuming run_pipeline returns a performance metric like accuracy
    performance = run_pipeline(amplitude, threshold_value)
    return -performance  # Minimize negative performance to maximize performance


def write_to_file(results_path, param, sa_best_params0, sa_best_params1, sa_best_score):
    raise NotImplementedError


def print_tex(results_path):
    raise NotImplementedError


def translate_to_hdev(graph):
    hdev_output = hdev_header

    for k in graph.keys():
        if k in hdev_functions.keys():
            hdev_output += "<l>    " + \
                           hdev_functions[k]['name'] + "(" + \
                           hdev_functions[k]['in'] + ", " + \
                           hdev_functions[k]['out'] + ", "
            i = 0
            for p in graph[k].keys():
                hdev_output += graph[k][p]
                i += 1
                if i < len(graph[k].keys()):
                    hdev_output += ", "

            hdev_output += ")</l>\n"

    hdev_output += hdev_footer

    return hdev_output


def write_hdev_code_to_file(file_path, hdev_code):
    hdev_path = hdev_folder + os.path.sep + \
                file_path.split(os.path.sep)[-4] + "-" + \
                file_path.split(os.path.sep)[-3] + "-" + \
                file_path.split(os.path.sep)[-2] + \
                ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path


def run_param_tuning() -> int:
    """
    Read the filter pipeline
    """
    pipeline_path = os.path.join("C:\\", "dev", "experiments", "scripts", "results", "202302191650", "Grid", "2",
                             "pipeline.txt")

    results_path = p_join(os.path.curdir, '../scripts/results')

    dot_content = read_dot_file(pipeline_path)

    graph = parse_dot(dot_content)

    hdev_code = translate_to_hdev(graph)

    hdev_path = write_hdev_code_to_file(pipeline_path, hdev_code)

    os.system("hdevelop -run " + hdev_path)

    """
    Simulated Annealing
    """
    # Define the parameter bounds: [amplitude_bounds, threshold_bounds]
    bounds = np.array([[-128, 128], [0, 255]])
    sa_best_params0, sa_best_params1, sa_best_score = run_simulated_annealing(objective, bounds)

    write_to_file(results_path, 'sa', sa_best_params0, sa_best_params1, sa_best_score)
    """
    Local Search
    """
    ls_best_params0, ls_best_params1, ls_best_score = run_local_search(objective, bounds)

    write_to_file(results_path, 'ls', ls_best_params0, ls_best_params1, ls_best_score)

    """
    Write Latex
    """
    print_tex(results_path)
    """
    file_path (source) | Algorithm | sa_best_params0 | sa_best_params1 | sa_best_score
    """


if __name__ == '__main__':
    run_param_tuning()
    # next section explains the use of sys.exit
    sys.exit()
