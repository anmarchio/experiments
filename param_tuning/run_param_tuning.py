import os
import sys

from api.database import Database
from api.models import Dataset
from param_tuning.data_handling import load_data, get_scores
from param_tuning.hdev.hdev_helpers import translate_to_hdev
from param_tuning.local_search import run_local_search
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import write_hdev_code_to_file, write_to_file, \
    get_pipeline_folder_name_by_datetime, write_csv_and_tex, dataset_to_graphs, write_digraph_to_files
from settings import HDEV_RESULTS_PATH, PARAM_TUNING_RESULTS_PATH


def run_pipeline(graph, params):
    hdev_code = translate_to_hdev(graph, params)

    raise NotImplementedError("Function not implemented correctly!")
    """
    TO DO
    -----
    - decode the path correctly!
    - include correct bounds
    - make sure to include `all` MVTec nodes/algorithms
    """
    hdev_path = write_hdev_code_to_file(graph['datetime'], hdev_code)

    prediction_path = os.path.join(HDEV_RESULTS_PATH, get_pipeline_folder_name_by_datetime(graph['datetime']))
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


def show_param_tuning_menu():
    print("\n")
    print("-" * 35)
    print("FOLLOW UP OPTIMIZATION using SA /LS")
    print("-" * 35)
    print("1 -- MANUAL 1: Export digraphs to txt")
    print("2 -- MANUAL 2: Read manual HDEV files and perform SA/LS")
    print("3 -- AUTOMATIC: Read DB and apply HDEV optimization")
    print("0 -- EXIT")

    print("\n")
    selection = input("Selection: ")
    if 0 < int(selection) < 4:
        return int(selection)
    return 0


def run_param_tuning() -> int:
    selection = show_param_tuning_menu()

    # Exit program
    if selection == 0:
        return 0

    # Get database object from api.database
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

    # Get the datasets per experiment in a dict
    experiment_datasets = {}
    if 0 < selection < 4:
        print("Really each pipeline?!?")
        raise ValueError("REALLY: EACH Pipeline?")
        experiment_datasets = Dataset.get_pipeline_by_each_dataset(db.get_session())

    if selection == 1:
        # 2 -- MANUAL 1: Export digraphs to txt

        # the output folder for digraphs
        digraph_path = test / manual_hdev_files

        for ds_id in experiment_datasets.keys():
            dataset = experiment_datasets[ds_id]

            # Write digraphs to folder
            write_digraph_to_files(dataset, digraph_path)

    if selection == 2:
        # 3 -- MANUAL 2: Read manual HDEV files and perform SA/LS

        manual_hdev_path = test / manual_hdev

        for hdev in os.listdir(manual_hdev_path):
            run_simulated_annealing()
            run_local_search()

    if selection == 3:
        # 1 -- AUTOMATIC: Read DB and apply HDEV optimization
        for ds_id in experiment_datasets.keys():
            dataset = experiment_datasets[ds_id]

            graphs = dataset_to_graphs(dataset)
            """"
            Convert pipeline to dict:
        
                graph = {
                    'training_path': None,
                    'result_path': None
                    'datetime': None,
                    'pipeline': pipeline.digraph
                }
            """

            for key in graphs.keys():
                algorithms = [
                    "sa",
                    "ls"
                ]

                best_params = []
                best_score = 0.0

                for algorithm in algorithms:
                    if algorithm == "sa":
                        # Simulated Annealing
                        best_params, best_score = run_simulated_annealing(graphs[key], objective)
                    elif algorithm == "ls":
                        # Local Search
                        best_params, best_score = run_local_search(graphs[key], objective)

                    write_to_file(PARAM_TUNING_RESULTS_PATH, algorithm, graphs[key]['training_path'],
                                  graphs[key]['datetime'],
                                  graphs[key]['path'],
                                  best_params,
                                  best_score)

            """
            Write to Latex Table:
                file_path (source) | Algorithm | sa_best_params0 | sa_best_params1 | sa_best_score
            """
            if len(dataset['best_pipelines']) > 0:
                write_csv_and_tex(PARAM_TUNING_RESULTS_PATH)

    return 0


if __name__ == '__main__':
    run_param_tuning()
    sys.exit()
