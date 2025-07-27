from param_tuning.dataset_pipeline_analysis import run_pipeline
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds
from param_tuning.utils import dataset_to_graphs


def run_pipeline_on_dataset(pipeline_name, graph):
    bounds = get_manual_hdev_pipeline_bounds(pipeline_name)

    try:
        score = run_pipeline(pipeline_name,
                             graph,
                             bounds)

        print(f"Resulting performance: {-score}")
        return score
    except Exception as e:
       print(e)
       write_to_log(pipeline_name, str(e))
       return [], [], 0.0


def read_db_and_cross_apply_hdev_pipelines(experiment_datasets):
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
            score = 0.0
            # pick cross-datasets minus the current
            for cross_dataset in [experiment_datasets.keys()-ds_id]:
                score = run_pipeline_on_dataset(graphs[key], cross_dataset)

                write_to_file(CROSS_APPLICATION_RESULTS_PATH,
                    graphs[key]['training_path'],
                    graphs[key]['datetime'],
                    graphs[key]['path'],
                    cross_dataset,
                    score)

        """
        Write to Latex Table:
            file_path (source) | score | cross-path (target) | score
        """
        if len(dataset['best_pipelines']) > 0:
            write_csv_and_tex(CROSS_APPLICATION_RESULTS_PATH)