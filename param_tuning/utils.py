import os
from datetime import datetime

from param_tuning.read_dot import parse_dot
from settings import HDEV_RESULTS_PATH, RESULTS_PATH


def raw_source_directory(dataset_source_directory):
    replace_strings = ["\"",
                       "D:\\evias_expmts\\",
                       "/mnt/sdc1/",
                       "C:\\Users\\Public\\evias_expmts\\\\",
                       "C:\\Users\\Public\\evias_expmts\\"]

    for item in replace_strings:
        dataset_source_directory = dataset_source_directory.replace(item, "")

    dataset_source_directory = dataset_source_directory.replace("\\", os.sep)
    dataset_source_directory = dataset_source_directory.replace("/", os.sep)

    if dataset_source_directory == "unknown":
        return None

    return dataset_source_directory


def dataset_to_graphs(dataset: {}) -> {}:
    graphs = {}

    for i in range(len(dataset['best_pipelines'])):
        graphs[str(i)] = {
            'training_path': raw_source_directory(dataset['source']),
            'results_path': RESULTS_PATH,  # <= has to be the date and time?
            'datetime': dataset['runs_created_at'][i],
            'pipeline': parse_dot(dataset['best_pipelines'][i][0].digraph)
        }

    return graphs


def write_digraph_to_files(dataset: {}, path: str) -> int:
    # Only get the last pipeline's digraph from the list
    digraph = dataset['best_pipelines'][-1][0].digraph

    filename = dataset['runs_created_at'][-1] + ".txt"

    f = open(os.path.join(path, filename), "a")
    f.write(digraph)
    f.close()

    return 0


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


def get_pipeline_folder_name_by_datetime(date_object):
    # testtime = "2022-11-19 13:19:50.000000"
    # date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return HDEV_RESULTS_PATH + os.path.sep + date_object.strftime("%Y%m%d%H%M")


def write_hdev_code_to_file(date_object, hdev_code) -> str:
    hdev_path = get_pipeline_folder_name_by_datetime(date_object) + ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path
