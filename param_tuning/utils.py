import os
from datetime import datetime

from settings import PARAM_TUNING_HDEV_MANUAL, EVIAS_SRC


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


def get_evias_experimts_path_for_hdev():
    source_path = ""
    for elmnt in EVIAS_SRC:
        source_path += elmnt + "/"
    return source_path


def check_dir_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def index_closest_to_mean(list_of_values, mean):
    if len(list_of_values) < 1:
        raise ValueError

    if len(list_of_values) == 1:
        return 0

    dist = list_of_values[0] - mean
    min_dist_idx = 0

    for idx in range(len(list_of_values)):
        new_dist = list_of_values[idx] - mean
        if new_dist < dist:
            dist = new_dist
            min_dist_idx = idx

    return min_dist_idx


def write_digraph_to_files(dataset_name: str, dataset_digraph: {}, path: str) -> int:
    if len(dataset_digraph.keys()) == 0:
        return 1

    content = "dataset: " + dataset_name + "\n\n"
    content += "experiment_id: " + str(dataset_digraph['experiment_id']) + "\n"
    content += "run_id: " + str(dataset_digraph['experiment_id']) + "\n"
    content += "fit_values: [" + str(dataset_digraph['best_individual_fitness']) + "]\n"
    content += "pipeline_id: " + str(dataset_digraph['pipeline_id']) + "\n\n"
    content += "digraph:\n" + str(dataset_digraph['digraph']) + "\n"

    filename = dataset_name + "_mean_pipeline.txt"

    f = open(os.path.join(path, filename), "w")
    f.write(content)
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
                "\\caption{\\textcolor{magenta}{Segmentation results of optimization heuristics applied for parameter " \
                "tuning on CGP outputs; the optimizers comprise \\textit{local search (LS)} and \\textit{simmulated " \
                "annealing (SA)}}}" + \
                "   \\label{tab:further_optimization}" + \
                "   \\resizebox{0.4\columnwidth}{!}{%" + \
                "       \\begin{tabular}{c l l l c c c c}" + \
                "           \\toprule" + \
                "\\textbf{Date} & \\textbf{Dataset} & \\textbf{Expmt Date} & $\overline{Path}$ & \\textbf{Best " \
                "Params} & \\textbf{Best Scores} \\\\" + \
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


def write_to_file(filepath, content):
    f = open(filepath, "a")
    f.write(content)
    f.close()


def write_log(iteration, performance, parameters, algorithm, pipeline_name, criterion="MCC"):
    filepath = os.path.join(PARAM_TUNING_HDEV_MANUAL, pipeline_name + ".txt")
    line = f"{iteration};{performance};{criterion};{parameters};{algorithm};{pipeline_name};{datetime.now()};\n"
    write_to_file(filepath, line)


def write_header_to_log(pipeline_name):
    filepath = os.path.join(PARAM_TUNING_HDEV_MANUAL, pipeline_name + ".txt")
    header = "Iteration; Performance; Criterion; Parameters; Algorithm; Pipeline; Datetime;\n"
    write_to_file(filepath, header)
