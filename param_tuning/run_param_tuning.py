import json
import sys
import os

from api.models import Dataset
from local_search import run_local_search
from param_tuning.data_handling import load_data, get_scores
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import extract_bounds_from_graph, translate_to_hdev, write_hdev_code_to_file, write_to_file, \
    print_tex, get_pipeline_folder_name
from read_dot import parse_dot
from settings import source_json_path, pipeline_txt_path, results_path, HDEV_RESULT


def run_pipeline(graph, params):
    hdev_code = translate_to_hdev(graph, params)

    raise NotImplementedError
    """
    TO DO
    -----
    - decode the path correctly!
    - include correct bounds
    - make sure to include `all` MVTec nodes/algorithms
    """
    hdev_path = write_hdev_code_to_file(graph['path'], hdev_code)

    prediction_path = os.path.join(HDEV_RESULT, get_pipeline_folder_name(graph['path']))
    if not os.path.exists(prediction_path):
        os.mkdir(prediction_path)

    # Execute Pipeline
    os.system("hdevelop -run " + hdev_path)

    # Evaluate Results
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
    performance = run_pipeline(graph, params)

    return -performance  # Minimize negative performance to maximize performance


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


def get_pipeline_from_data_structure():
    """
    Read the filter pipeline
    """
    pipeline = parse_dot(get_pipeline_dot_content())
    pipeline['path'] = raw_source_directory(get_dataset_source_directory())
    pipeline['datetime'] = pipeline_txt_path.split(os.sep)[-4]

    return pipeline


def run_sa_experiments():
    pipeline = get_pipeline_from_data_structure()

    """
    Simulated Annealing
    """
    sa_best_params, sa_best_score = run_simulated_annealing(pipeline, objective)

    write_to_file(results_path, 'sa', pipeline['training_path'], pipeline['datetime'], pipeline['path'], sa_best_params,
                  sa_best_score)

    """
    Write Latex
    """
    # print_tex(results_path)
    """
    file_path (source) | Algorithm | sa_best_params0 | sa_best_params1 | sa_best_score
    """
    return 0


def run_ls_experiments() -> int:
    pipeline = get_pipeline_from_data_structure()
    raise NotImplementedError
    """
    Local Search
    """
    ls_best_params, ls_best_score = run_local_search(pipeline, objective)

    write_to_file(results_path, 'ls', pipeline['training_path'], pipeline['datetime'], pipeline['path'], ls_best_params,
                  ls_best_score)

    return 0


def run_param_tuning() -> int:
    """
    TO DO
    =====
    - walk through database
    - Select pipeline entry
    - feed to run_sa_experiments
    """
    raise ValueError
    experiment_datasets = Dataset.get_runs_pipeline_by_each_dataset()

    run_sa_experiments(experiment_datasets)

    run_ls_experiments(experiment_datasets)

    return 0


if __name__ == '__main__':
    run_param_tuning()
    # next section explains the use of sys.exit
    sys.exit()
