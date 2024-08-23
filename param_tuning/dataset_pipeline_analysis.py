import os

import numpy as np

from api.database import Database
from api.models import Dataset, Pipeline
from dashboard.utils import data_linking
from param_tuning.data_handling import get_scores
from param_tuning.hdev.hdev_helpers import translate_graph_to_hdev
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline
from param_tuning.local_search import run_local_search
from param_tuning.read_dot import parse_dot
from param_tuning.simulated_annealing import run_simulated_annealing
from param_tuning.utils import raw_source_directory, index_closest_to_mean, write_to_file, write_csv_and_tex
from settings import RESULTS_PATH, HDEV_RESULTS_PATH, PARAM_TUNING_RESULTS_PATH


def run_pipeline(pipeline_name: str, graph: {} = None, param: np.array, manual: bool = True):
    hdev_code = ""
    hdev_path = ""

    if manual:
        hdev_code = get_manual_hdev_pipeline(pipeline_name, params)
        hdev_path = get_manual_hdev_pipeline_path(pipeline_name)
    else:
        hdev_code = translate_graph_to_hdev(graph, params)
        hdev_path = write_hdev_code_to_file(graph['datetime'], hdev_code)


    #raise NotImplementedError("Function not implemented correctly!")
    """
    TO DO
    -----
    - decode the path correctly!
    - include correct bounds
    - make sure to include `all` MVTec nodes/algorithms
    """

    prediction_path = os.path.join(HDEV_RESULTS_PATH, get_pipeline_folder_name_by_datetime(graph['datetime']))
    if not os.path.exists(prediction_path):
        os.mkdir(prediction_path)

    # Execute Pipeline
    os.system("hdevelop -run " + hdev_path)

    # Evaluate Results
    if manual:
        labels_arr, predictions_arr = load_data(graph['training_path'] + "labels", prediction_path)
    else:
        labels_arr, predictions_arr = load_data(training_path + "labels", prediction_path)
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


def objective(pipeline_name, graph, params, manual = True):
    # Run the pipeline with given parameters and evaluate performance
    # Performance is returned as intersection over union (IoU) / Jaccard Score
    performance = run_pipeline(pipeline_name, graph, params, manual)

    return -performance  # Minimize negative performance to maximize performance


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


def get_analyzer_id_by_index_in_dataset_dict(dataset_dict: {}, mean_idx: int):
    idx = 0
    for d in dataset_dict:
        for r in d["values"]:
            if idx == mean_idx:
                return r[-1].analyzer_id
            idx += 1


def write_hdev_code_to_file(date_object, hdev_code) -> str:
    hdev_path = get_pipeline_folder_name_by_datetime(date_object) + ".hdev"

    f = open(hdev_path, "w")
    f.write(hdev_code)
    f.close()

    return hdev_path


def get_pipeline_folder_name_by_datetime(date_object):
    # testtime = "2022-11-19 13:19:50.000000"
    # date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return HDEV_RESULTS_PATH + os.path.sep + date_object.strftime("%Y%m%d%H%M")


def get_grouped_datasets_with_digraph_by_mean_fitness(session: Database):
    """
        Retrieves and processes fitness data from grouped datasets to associate each group with its mean fitness value
        and corresponding pipeline digraph.

        This function performs the following steps:
        1. Fetches fitness data for runs grouped by datasets.
        2. Links and processes this data to compute mean fitness values for each group.
        3. For each group, identifies the fitness value closest to the mean and retrieves the corresponding analyzer ID.
        4. Uses the analyzer ID to obtain pipeline details and digraph.
        5. Compiles results into a dictionary mapping each group to its mean fitness value and associated pipeline information.

        Args:
            session (Database): The database session used to query and retrieve data.

        Returns:
            dict: A dictionary where keys are dataset group identifiers and values are dictionaries containing:
                  - 'experiment_id': ID of the experiment associated with the group.
                  - 'run_id': ID of the run associated with the group.
                  - 'best_individual_fitness': Fitness value closest to the mean for the group.
                  - 'pipeline_id': ID of the pipeline associated with the group.
                  - 'digraph': Directed graph (digraph) of the pipeline associated with the group.
    """
    linked_list_of_mean_fitness_and_digraph = {}

    # Grouped_dataset
    list_of_runs_fitness = Dataset.get_runs_fitness_by_grouped_dataset(session, 140, 500)

    linked_list_of_runs_fitness = data_linking(list_of_runs_fitness)

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

        # Abort this loop if mean_fit is empty
        if np.isnan(mean_fit):
            continue

        # Get idx of array for fitness closest to mean
        mean_idx = index_closest_to_mean(fit_values, mean_fit)

        # Get analyzer_id from right idx within several 'runs' in dataset experiments
        analyzer_id = get_analyzer_id_by_index_in_dataset_dict(linked_list_of_runs_fitness[k], mean_idx)

        experiment_id, run_id, pipeline_id, digraph = Pipeline.get_pipeline_by_analyzer(session,
                                                                                        analyzer_id)
        linked_list_of_mean_fitness_and_digraph[k] = {
            'experiment_id': experiment_id,
            'run_id': run_id,
            'best_individual_fitness': fit_values[mean_idx],
            'pipeline_id': pipeline_id,
            'digraph': digraph
        }

    return linked_list_of_mean_fitness_and_digraph


def read_db_and_apply_algorithms_to_hdev(experiment_datasets):
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
