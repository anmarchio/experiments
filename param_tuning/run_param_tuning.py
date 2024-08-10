import json
import sys
import os

from local_search import run_local_search
from param_tuning.data_handling import load_data, get_scores
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import extract_bounds_from_graph, translate_to_hdev, write_hdev_code_to_file, write_to_file, \
    print_tex
from read_dot import read_dot_file, parse_dot
from settings import source_json_path, pipeline_txt_path, results_path, HDEV_RESULT


def run_pipeline(graph):
    # Define the parameter bounds: [amplitude_bounds, threshold_bounds]
    bounds = extract_bounds_from_graph(graph)

    hdev_code = translate_to_hdev(graph)

    # raise NotImplementedError
    hdev_path = write_hdev_code_to_file(graph['path'], hdev_code)

    # Execute Pipeline
    os.system("hdevelop -run " + hdev_path)
    raise NotImplementedError
    """
    TO DO:
    - create 'pipeline-date' folder
    - write prediction images to this folder
    - labels_path = os.path.join("C:\\","evias_expmts", source_path, ") 
    - prediction_path = os.path.join(HDEV_FOLDER, date) 
    """

    # Evaluate Results
    prediction_path = os.path.join(HDEV_RESULT, "out")
    labels_arr, predictions_arr = load_data(graph['training_path'] + "labels", prediction_path)
    scores = get_scores(labels_arr, predictions_arr)
    """
    scores = {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "mcc": mcc,
        "f1": f1,
        "jaccard": iou,
        "accuracy": accuracy
    }
    """

    return scores['jaccard']


def objective(graph, params):
    # Run the pipeline with given parameters and evaluate performance
    # Performance is returned as intersection over union (IoU) / Jaccard Score
    performance = run_pipeline(graph)

    return -performance  # Minimize negative performance to maximize performance


def run_param_tuning() -> int:
    """
    Read the filter pipeline
    """
    dot_content = read_dot_file(pipeline_txt_path)

    pipeline = parse_dot(dot_content)

    pipeline['path'] = pipeline_txt_path
    pipeline['datetime'] = pipeline_txt_path.split(os.sep)[-4]

    with open(source_json_path, 'r') as file:
        data = json.load(file)
    pipeline['training_path'] = data[0]['trainingDataDirectory']

    """
    Simulated Annealing
    """
    sa_best_params, sa_best_score = run_simulated_annealing(pipeline, objective)

    write_to_file(results_path, 'sa', sa_best_params, sa_best_score)
    """
    Local Search
    """
    ls_best_params, ls_best_score = run_local_search(pipeline, objective)

    write_to_file(results_path, 'ls', ls_best_params, ls_best_score)

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
