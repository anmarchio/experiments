import os

from param_tuning.dataset_pipeline_analysis import run_pipeline
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds, MANUAL_HDEV_PIPELINES_MEAN
from param_tuning.utils import write_log, check_dir_exists
from settings import CROSS_APPLICATION_RESULTS_PATH, CROSS_APPLICATION_HDEV_MANUAL


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
        write_log(CROSS_APPLICATION_RESULTS_PATH, pipeline_name, str(e))
        return [], [], 0.0


def write_to_file(filepath, content):
    f = open(filepath, "a")
    f.write(content)
    f.close()


def write_cross_application_header_to_log(pipeline_name):
    filepath = os.path.join(CROSS_APPLICATION_HDEV_MANUAL, pipeline_name + ".txt")
    header = "Pipeline; OriginalScore; CrossApplication; CrossScore;\n"
    write_to_file(filepath, header)


def write_cross_application_log(pipeline_name, log_content):
    filepath = os.path.join(CROSS_APPLICATION_HDEV_MANUAL, pipeline_name + ".txt")
    write_to_file(filepath, log_content)
