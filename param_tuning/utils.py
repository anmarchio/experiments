import os

import numpy as np

from datetime import datetime
from param_tuning.hdev.hdev_template import HDEV_FUNCTIONS, HDEV_HEADER, HDEV_FOOTER, HDEV_TEMPLATE_CODE
from settings import HDEV_RESULTS_PATH


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


def write_to_file(result_file_path, algorithm, source, experiment_datetime, experiment_path, best_params, best_score):
    # def save_scores_to_db(scores: [], model_name: str, root_path: str, dataset_path: {}):
    # existing_results = load_results(RESULTS_DB_PATH)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """
    new_results = [
        {
            #"ID": str(len(existing_results)),
            "datetime": current_datetime,
            "algorithm": algorithm,
            "source": source,
            "experiment_datetime": experiment_datetime,
            "experiment_path": experiment_path,
            "best_params": best_params,
            "best_score": best_score
        }
    ]
    # existing_results.extend(new_results)
    # save_results(existing_results, RESULTS_DB_PATH)
    """
    line = ""

    if not os.path.exists(result_file_path):
        line = "datetime; source; experiment_datetime; experiment_path; best_params; best_score;\n"

    line += current_datetime + ";" + \
            algorithm + ";" + \
            source + ";" + \
            experiment_datetime + ";" + \
            experiment_path + ";" + \
            best_params + ";" + \
            best_score + ";\n"

    f = open(result_file_path + ".csv", "a")
    f.write(line)
    f.close()


def write_csv_and_tex(read_from_path: str):
    if not os.path.exists(read_from_path):
        return 0

    f = open(read_from_path + ".csv", "r")
    lines = f.readlines()

    tex_table = "\\begin{table}[h]\n" + \
                "   \\centering" + \
                "   \\caption{\\textcolor{magenta}{Segmentation results of optimization heuristics applied for parameter tuning on CGP outputs; the optimizers comprise \\textit{local search (LS)} and \\textit{simmulated annealing (SA)}}}" + \
                "   \\label{tab:further_optimization}" + \
                "   \\resizebox{0.4\columnwidth}{!}{%" + \
                "       \\begin{tabular}{c l l l c c c c}" + \
                "           \\toprule" + \
                "           \\textbf{Date} & \\textbf{Dataset} & \\textbf{Expmt Date} & $\overline{Path}$ & \\textbf{Best Params} & \\textbf{Best Scores} \\\\" + \
                "           \\midrule\n"

    for i in range(len(lines)):
        if i > 0:
            cols = f.readline().split(";")
            # header = "datetime; source; experiment_datetime; experiment_path; best_params; best_score;\n"

            tex_table += "           "

            for c in range(len(cols)):
                tex_table += cols[c]

                if c < len(cols) - 1:
                    tex_table += " &"

                tex_table += "\\\\\n"

    tex_table += "			\\bottomrule" + \
                 "		\\end{tabular}" + \
                 "	}" + \
                 "\\end{table}"
    f.close()

    print(tex_table)
    fw = open(read_from_path + ".txt", "w")
    fw.write(tex_table)
    fw.close()


def translate_to_hdev(graph, params):
    # HDEV xml style header
    hdev_output = HDEV_HEADER

    # define source and output path for reading image and writing results (binary images)
    hdev_output += "<l>source_path := '" + graph['training_path'].replace("\\", "/") + "/images'</l>\n"

    hdev_output += "<l>output_path := '"
    hdev_output += graph['datetime'].strftime("%Y%m%d%H%M").replace("\\", "/") + "'</l>\n"

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


def get_pipeline_folder_name_by_datetime(date_string):
    # testtime = "2022-11-19 13:19:50.000000"
    date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return HDEV_RESULTS_PATH + os.path.sep + date_object.strftime("%Y%m%d%H%M")


def write_hdev_code_to_file(date_string: str, hdev_code: str) -> str:
    hdev_path = get_pipeline_folder_name_by_datetime(date_string) + ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path
