import os

import numpy as np

from param_tuning.hdev.hdev_template import HDEV_FUNCTIONS, HDEV_HEADER, HDEV_FOOTER, HDEV_FOLDER


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


def write_to_file(results_path, param, sa_best_params, sa_best_score):
    raise NotImplementedError


def print_tex(results_path):
    raise NotImplementedError


def translate_to_hdev(graph):
    hdev_output = HDEV_HEADER

    for k in graph.keys():
        if k in HDEV_FUNCTIONS.keys():
            hdev_output += "<l>    " + \
                           HDEV_FUNCTIONS[k]['name'] + "(" + \
                           HDEV_FUNCTIONS[k]['in'] + ", " + \
                           HDEV_FUNCTIONS[k]['out'] + ", "
            i = 0
            for p in graph[k].keys():
                hdev_output += graph[k][p]
                i += 1
                if i < len(graph[k].keys()):
                    hdev_output += ", "

            hdev_output += ")</l>\n"

    hdev_output += HDEV_FOOTER

    return hdev_output


def write_hdev_code_to_file(file_path: object, hdev_code: object) -> object:
    hdev_path = HDEV_FOLDER + os.path.sep + \
                file_path.split(os.path.sep)[-4] + "-" + \
                file_path.split(os.path.sep)[-3] + "-" + \
                file_path.split(os.path.sep)[-2] + \
                ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path
