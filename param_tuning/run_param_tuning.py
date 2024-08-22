import os
import sys

import numpy as np

from api import env_var
from api.database import Database
from api.models import Dataset, Pipeline
from dashboard.utils import data_linking, compute_mean_and_std_dev
from param_tuning.data_handling import load_data, get_scores
from param_tuning.hdev.hdev_helpers import translate_to_hdev
from param_tuning.local_search import run_local_search
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import write_hdev_code_to_file, write_to_file, \
    get_pipeline_folder_name_by_datetime, write_csv_and_tex, dataset_to_graphs, write_digraph_to_files, \
    check_dir_exists, index_closest_to_mean
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
    try:
        if 0 < int(selection) < 4:
            return int(selection)
    except:
        selection = 0
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
        print("Pipeline by grouped Dataset closest to mean fitness")
        print("-- from DB path: " + env_var.SQLITE_PATH)
        list_of_runs_fitness = {}

        # Grouped_dataset
        list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(db.get_session(), 140, 500)

        linked_list_of_runs_fitness = data_linking(list_of_runs_fitness)

        # !!!this has to be removed!!!
        # list_of_runs_fitness_pipelines = Dataset.get_pipeline_fitness_by_grouped_dataset(db.get_session(), 140, 500)

        linked_list_of_fitness_and_digraph = {}
        cnt = 0
        for k in linked_list_of_runs_fitness.keys():
            run_ids = [d['id'] for d in linked_list_of_runs_fitness[k]]
            if len(linked_list_of_runs_fitness[k]) > 0:
                print("ID: ", str(run_ids), ", reading ...")
            else:
                print("ID: ", str(run_ids), ", [EMPTY ENTRY]")
                continue
            cnt += 1
            fit_values = []
            for d in linked_list_of_runs_fitness[k]:
                for r in d["values"]:
                    fit_values.append([f.best_individual_fitness for f in r][-1])
            mean_fit = np.mean(fit_values)
            print("Find pipeline")
            if np.isnan(mean_fit):
                continue
            mean_idx = index_closest_to_mean(fit_values, mean_fit)
            analyzer_id = d["values"][mean_idx][-1].analyzer_id
            print("analyzer_id: " + str(analyzer_id))
            """
            NOTE:
            MVTEC_XYZ 
                > 0, 1, 2 (experiment reptitions)
                    > values 1,2,3 (runs)
            => walk through all experiments, 
                THEN through the runs
            => get pipeline
            """
            experiment_id, run_id, pipeline_id, digraph = Pipeline.get_pipeline_by_analyzer(db.get_session(), analyzer_id)
            linked_list_of_fitness_and_digraph[k] = {
                'experiment_id': experiment_id,
                'run_id': run_id,
                'best_individual_fitness': fit_values[mean_idx],
                'pipeline_id': pipeline_id,
                'digraph': digraph
            }

        for ds_key in linked_list_of_fitness_and_digraph.keys():
            dataset_digraph = linked_list_of_fitness_and_digraph[ds_key]
            """
            CHANGE:
            use digraph, fitness and ID to write to file
            """
            # Write digraphs to folder
            write_digraph_to_files_NEW(ds_key, dataset_digraph)

    if selection == 1:
        # 1 -- MANUAL 1: Export digraphs to txt

        # output folder for digraphs
        digraph_path = os.path.join(PARAM_TUNING_RESULTS_PATH, "digraphs")
        check_dir_exists(PARAM_TUNING_RESULTS_PATH)
        check_dir_exists(digraph_path)

        for ds_id in experiment_datasets.keys():
            dataset = experiment_datasets[ds_id]

            # Write digraphs to folder
            write_digraph_to_files(dataset, digraph_path)

    if selection == 2:
        # 2 -- MANUAL 2: Read manual HDEV files and perform SA/LS
        manual_hdev_path = os.path.join(PARAM_TUNING_RESULTS_PATH, "manual_hdev")
        check_dir_exists(PARAM_TUNING_RESULTS_PATH)
        check_dir_exists(manual_hdev_path)

        raise NotImplementedError("NOT IMPLEMENTED!")

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
