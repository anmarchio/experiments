import os

import matplotlib.pyplot as plt
import numpy as np

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


def format_line(iteration, performance, parameters, algorithm, configuration, pipeline_name, criterion="mcc"):
    return f"{iteration};{performance};{criterion};{parameters};{algorithm};{configuration};{pipeline_name};{datetime.now()};\n"


def write_log(pipeline_name, log_content):
    filepath = os.path.join(PARAM_TUNING_HDEV_MANUAL, pipeline_name + ".txt")
    write_to_file(filepath, log_content)


def write_header_to_log(pipeline_name):
    filepath = os.path.join(PARAM_TUNING_HDEV_MANUAL, pipeline_name + ".txt")
    header = "Iteration; Performance; Criterion; Parameters; Algorithm; Configuration; Pipeline; Datetime;\n"
    write_to_file(filepath, header)


def get_dummy_data_rows():
    # Dummy data for testing
    datasets = [
        'capsule_crack', 'durchlauf1', 'zipper_rough', 'tile_crack',
        'screw_scratch_neck', 'bottle_broken_lg', 'carpet', 'leather',
        'fabric_defects_aitex', 'spule0-0315_upside'
    ]
    cgp_results = [0.23, 0.45, 0.35, 0.4, 0.3, 0.35, 0.32, 0.25, 0.38, 0.34]
    ls_results = [cgp + np.random.uniform(0.01, 0.2) for cgp in cgp_results]
    sa_results = [ls + np.random.uniform(0.01, 0.2) for ls in ls_results]
        
    return datasets, cgp_results, ls_results, sa_results
        
    
    
def plot_fitness_bars(datasets, cgp_results, ls_results, sa_results):
    # Plot Bar Chart of CGP vs. LS/SA results
    # ---------------------------------------
    
    # Number of datasets
    num_datasets = len(datasets)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Bar width
    bar_width = 0.25

    # The y positions for each dataset
    y_pos = np.arange(num_datasets)

    # Plotting the bars
    ax.barh(y_pos, cgp_results, color='blue', height=bar_width, label='CGP Result')
    ax.barh(y_pos + bar_width, ls_results, color='lightcoral', height=bar_width, label='LS Result')
    ax.barh(y_pos + 2 * bar_width, sa_results, color='lightgray', height=bar_width, label='SA Result')

    # Setting the y ticks with dataset names
    ax.set_yticks(y_pos + bar_width)
    ax.set_yticklabels(datasets)

    # Adding labels and title
    ax.set_xlabel('Result')
    ax.set_title('Results Comparison by Dataset')
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()


def plot_changes_bars(datasets, changes):
    # Plot Changes (+/-) for CGP vs. LS/SA results    
    # ---------------------------------------
    
    # Create color array based on positive or negative changes
    colors = ['lightblue' if change >= 0 else 'lightcoral' for change in changes]
    
    # Create a horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(datasets, changes, color=colors)

    # Add title and labels
    plt.title('Fitness Net Increase')
    plt.xlabel('Change in Fitness')
    plt.ylabel('Dataset')

    # Set x-axis limits for changes plot (-0.5 to +0.5)
    plt.xlim(-0.5, 0.5)

    # Display grid
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()
    
 
 
def plot_bar_charts(datasets, cgp_results, ls_results, sa_results):
    # TESTING
    # overwrite variables with DUMMY data
    datasets, cgp_results, ls_results, sa_results = get_dummy_data_rows()
        
    changes = [max(ls_results[i] - cgp_results[i], sa_results[i] - cgp_results[i]) for i in range(len(cgp_results))]
    
    plot_fitness_bars(datasets, cgp_results, ls_results, sa_results)
    plot_changes_bars(datasets, changes)
    
def extract_fitness_values(file_paths):
    sa_results = []
    ls_results = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # Filter out the relevant lines for SA and LS
            sa_best = None
            ls_best = None

            for line in lines:
                parts = line.strip().split(';')
                if isinstance(parts[0], (int, np.int32, float)):
                    if len(parts) >= 5:  # Ensure line has enough parts to be valid
                        iteration = int(parts[0].strip())
                        performance = float(parts[1].strip())
                        algorithm = parts[4].strip().lower()

                        # Assuming the last iteration (99) has the best performance
                        if iteration == 99:
                            if algorithm == 'sa':
                                sa_best = performance
                            elif algorithm == 'ls':
                                ls_best = performance
            
            # Append the best results to the lists
            if sa_best is not None:
                sa_results.append(sa_best)
            if ls_best is not None:
                ls_results.append(ls_best)

    return sa_results, ls_results
