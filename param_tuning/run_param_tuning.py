import os
import sys

from api.database import Database
from api.models import Dataset
from local_search import run_local_search
from param_tuning.data_handling import load_data, get_scores
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import translate_to_hdev, write_hdev_code_to_file, write_to_file, \
    get_pipeline_folder_name_by_datetime
from read_dot import parse_dot
from settings import RESULTS_PATH, HDEV_RESULTS_PATH, PARAM_TUNING_RESULTS_PATH


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
    hdev_path = write_hdev_code_to_file(graph['datetime'], hdev_code)

    prediction_path = os.path.join(HDEV_RESULT, get_pipeline_folder_name_by_datetime(graph['result_path']))
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


def get_graph_dict_from_pipeline(pipeline: str):
    graph = {
        'training_path': pipeline['source_directory'],
        'result_path': RESULTS_PATH,  # <= has to be the date and time?
        'datetime': pipeline['datetime'],
        'pipeline': parse_dot(pipeline.digraph)
    }

    return graph

def run_param_tuning() -> int:
    db = Database()

    """
    Dataset.get_runs_pipeline_by_each_dataset returns the dictionary as follows:

        datasets_pipeline_lists[ds.dataset_id] = {
            "id": ds.dataset_id,
            "name": ds.name,
            "source": ds.source_directory,
            "run_created_at": [e.created_at for e in experiment_runs],
            "best_pipelines": best_pipelines
        }
    """
    experiment_datasets = Dataset.get_pipeline_by_each_dataset(db.get_session())

    for dataset in experiment_datasets:
        print("Really each pipeline?!?")
        # raise ValueError("Really each pipeline?!?")

        for pipeline in dataset['best_pipelines']:
            """
            Convert pipeline to dict:

                graph = {
                    'training_path': None,
                    'result_path': None
                    'datetime': None,
                    'pipeline': pipeline.digraph
                }
            """
            graph = get_graph_dict_from_pipeline(pipeline)

            algorithms = [
                "sa",
                "ls"
            ]

            best_params = []
            best_score = 0.0

            for algorithm in algorithms:
                if algorithm == "sa":
                    # Simulated Annealing
                    best_params, best_score = run_simulated_annealing(graph, objective)
                elif algorithm == "ls":
                    # Local Search
                    best_params, best_score = run_local_search(graph, objective)

                write_to_file(PARAM_TUNING_RESULTS_PATH, algorithm, graph['training_path'], graph['datetime'],
                              graph['path'],
                              best_params,
                              best_score)

        """
        Write to Latex Table:
            file_path (source) | Algorithm | sa_best_params0 | sa_best_params1 | sa_best_score
        """
        write_csv_and_tex(PARAM_TUNING_RESULTS_PATH)

    return 0


if __name__ == '__main__':
    run_param_tuning()
    sys.exit()
