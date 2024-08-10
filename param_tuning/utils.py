import os

import numpy as np

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


def write_to_file(results_path, param, sa_best_params, sa_best_score):
    raise NotImplementedError


def print_tex(results_path):
    raise NotImplementedError


def translate_to_hdev(graph):
    # HDEV xml style header
    hdev_output = HDEV_HEADER

    # define source and output path for reading image and writing results (binary images)
    hdev_output += "<l>source_path := '" + graph['training_path'].replace("\\", "/") + "/images'</l>\n"

    hdev_output += "<l>output_path := '"
    for item in HDEV_RESULT.split(os.sep):
        hdev_output += item + "/"
    hdev_output += "'</l>\n"

    hdev_output += HDEV_TEMPLATE_CODE

    # decode pipeline and translate to hdev code
    # node by node from graph dict
    for k in graph['pipeline'].keys():
        if k in HDEV_FUNCTIONS.keys():
            hdev_output += "<l>    " + \
                           HDEV_FUNCTIONS[k]['name'] + "(" + \
                           HDEV_FUNCTIONS[k]['in'] + ", " + \
                           HDEV_FUNCTIONS[k]['out'] + ", "
            i = 0
            for p in graph['pipeline'][k].keys():
                hdev_output += graph['pipeline'][k][p]
                i += 1
                if i < len(graph['pipeline'][k].keys()):
                    hdev_output += ", "

            hdev_output += ")</l>\n"

    # add the footer hdev code
    # to write results to binary image
    hdev_output += HDEV_FOOTER

    return hdev_output


def write_hdev_code_to_file(file_path: object, hdev_code: object) -> object:
    hdev_path = HDEV_RESULT + os.path.sep + \
                file_path.split(os.path.sep)[-4] + "-" + \
                file_path.split(os.path.sep)[-3] + "-" + \
                file_path.split(os.path.sep)[-2] + \
                ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path
