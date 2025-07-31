import os

from param_tuning.hdev_manual.run_hdev_manual import MANUAL_HDEV_PIPELINES_MEAN, get_initial_state_by_pipeline_name
from param_tuning.utils import check_dir_exists
from pipeline_retrieval.cross_application_on_all_datasets import (run_pipeline_on_dataset,
                                                                  write_cross_application_header_to_log,
                                                                  write_cross_application_log)
from settings import CROSS_APPLICATION_RESULTS_PATH


def manual_cross_apply_hdev_pipelines():
    manual_hdev_path = os.path.join(CROSS_APPLICATION_RESULTS_PATH, "manual_hdev")
    check_dir_exists(CROSS_APPLICATION_RESULTS_PATH)
    check_dir_exists(manual_hdev_path)

    for pipeline_name in MANUAL_HDEV_PIPELINES_MEAN:
        write_cross_application_header_to_log(pipeline_name)

        try:
            graph = get_initial_state_by_pipeline_name(pipeline_name)
            original_score = run_pipeline_on_dataset(pipeline_name, graph)

            # pick cross-datasets minus the current
            for cross_dataset in [key for key in MANUAL_HDEV_PIPELINES_MEAN if key != pipeline_name]:

                try:
                    cross_score = run_pipeline_on_dataset(pipeline_name, graph, cross_dataset)
                    write_cross_application_log(pipeline_name,
                                                f"{pipeline_name};{original_score};{cross_dataset};{cross_score};\n")
                except Exception as e:
                    print(f"Error running cross dataset {cross_dataset} for pipeline {pipeline_name}: {e}\n")
                    write_cross_application_log(pipeline_name, f"ERROR: {e};\n")

        except Exception as e:
            print(f"Error running pipeline {pipeline_name}: {e}\n")
            write_cross_application_log(pipeline_name, f"FAILED: {e};\n")
            continue


def main():
    print("CGP Pipeline Cross Application")
    print("-" * 30)

    selection = input("Start the CGP pipeline cross application? (1 = yes)")

    # Exit program
    if selection == "0":
        print("Exiting ...")
        return 0

    # 4 -- Cross-apply cgp pipelines on all datasets (ca. 900 runs)
    if selection == "1":
        manual_cross_apply_hdev_pipelines()


if __name__ == "__main__":
    main()
