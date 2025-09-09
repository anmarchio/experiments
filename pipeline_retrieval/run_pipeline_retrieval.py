import os

from param_tuning.hdev_manual_best.run_hdev_manual_best import MANUAL_HDEV_PIPELINES_BEST
from param_tuning.hdev_manual_mean.run_hdev_manual_mean import MANUAL_HDEV_PIPELINES_MEAN
from param_tuning.run_hdev_manual import get_initial_state_by_pipeline_name
from param_tuning.utils import check_dir_exists
from pipeline_retrieval.cross_application_on_all_datasets import (run_pipeline_on_dataset,
                                                                  write_cross_application_header_to_log,
                                                                  write_cross_application_log)
from settings import CROSS_APPLICATION_RESULTS_PATH


def manual_cross_apply_hdev_pipelines(mean: bool = True,
                                           best: bool = False):
    """
    Cross-apply manual hdev pipelines on all datasets (ca. 900 runs).
    Only pipelines are used, which are defined in
    - MANUAL_HDEV_PIPELINES_MEAN
    - MANUAL_HDEV_PIPELINES_BEST
    """
    manual_hdev_path = os.path.join(CROSS_APPLICATION_RESULTS_PATH, "manual_hdev")
    check_dir_exists(CROSS_APPLICATION_RESULTS_PATH)
    check_dir_exists(manual_hdev_path)

    manual_hdev_pipelines = MANUAL_HDEV_PIPELINES_MEAN if mean else MANUAL_HDEV_PIPELINES_BEST

    for pipeline_name in manual_hdev_pipelines:
        write_cross_application_header_to_log(pipeline_name)

        try:
            graph = get_initial_state_by_pipeline_name(pipeline_name)
            original_score = run_pipeline_on_dataset(pipeline_name, graph)

            # pick cross-datasets minus the current
            for cross_dataset in [key for key in manual_hdev_pipelines if key != pipeline_name]:

                try:
                    cross_score = run_pipeline_on_dataset(pipeline_name, graph, cross_dataset)
                    write_cross_application_log(pipeline_name,
                                                f"{pipeline_name};{original_score};{cross_dataset};{cross_score};\n")
                except Exception as e:
                    print(f"Error running cross dataset {cross_dataset} for pipeline {pipeline_name}: {e}")
                    write_cross_application_log(pipeline_name, f"ERROR: {e};\n")

        except Exception as e:
            print(f"Error running pipeline {pipeline_name}: {e}")
            write_cross_application_log(pipeline_name, f"FAILED: {e};\n")
            continue


def main():
    print("CGP Pipeline Cross Application")
    print("-" * 30)
    print("1 - MEAN (by MCC) hdev pipeline cross application")
    print("2 - BEST (by MCC) hdev pipeline cross application")
    print("0 - Exit")
    selection = input("Selection: ")

    # Exit program
    if selection == "0":
        print("Exiting ...")
        return 0

    # 4 -- Cross-apply cgp pipelines on all datasets (ca. 900 runs)
    if selection == "1":
        manual_cross_apply_hdev_pipelines(mean = True)
    
    if selection == "2":
        print("BEST (by MCC) hdev pipeline cross application is not implemented yet.")
        manual_cross_apply_hdev_pipelines(mean = False, best = True)
        return 0


if __name__ == "__main__":
    main()
