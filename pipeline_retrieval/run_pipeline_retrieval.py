import os

from param_tuning.hdev_manual_best.run_hdev_manual_best import MANUAL_HDEV_PIPELINES_BEST
from param_tuning.hdev_manual_mean.run_hdev_manual_mean import MANUAL_HDEV_PIPELINES_MEAN
from param_tuning.run_hdev_manual import get_initial_state_by_pipeline_name
from param_tuning.utils import check_dir_exists
from pipeline_retrieval.cross_application_on_all_datasets import (run_pipeline_on_dataset,
                                                                  write_cross_application_header_to_log,
                                                                  write_cross_application_log)
from pipeline_retrieval.helpers import create_global_tracker
from settings import CROSS_APPLICATION_RESULTS_PATH


def manual_cross_apply_hdev_pipelines(mode: str = "mean"):
    """
    Cross-apply manual hdev pipelines on all datasets (ca. 900 runs).
    Only pipelines are used, which are defined in
    - MANUAL_HDEV_PIPELINES_MEAN
    - MANUAL_HDEV_PIPELINES_BEST
    """
    print("Cross-apply manual hdev pipelines on all datasets")
    print("="*20)
    print("Type of Pipelines (Mode): " + mode)

    manual_hdev_path = os.path.join(CROSS_APPLICATION_RESULTS_PATH, "manual_hdev")
    check_dir_exists(CROSS_APPLICATION_RESULTS_PATH)
    check_dir_exists(manual_hdev_path)

    # mean by default
    manual_hdev_pipelines = MANUAL_HDEV_PIPELINES_MEAN

    if mode == "best" or mode == "best_test":
        print("Evaluations: " + str((len(CROSS_APPLICATION_RESULTS_PATH)-1) * (len(MANUAL_HDEV_PIPELINES_BEST)-1)))
        print("Datasets:\n")
        print("\n".join(MANUAL_HDEV_PIPELINES_BEST))
        manual_hdev_pipelines = MANUAL_HDEV_PIPELINES_BEST
    else:
        print("Evaluations: " + str((len(CROSS_APPLICATION_RESULTS_PATH)-1) * (len(MANUAL_HDEV_PIPELINES_MEAN)-1)))
        print("Datasets:\n")
        print("\n".join(MANUAL_HDEV_PIPELINES_MEAN))

    cross_scores = [['from', 'applied on', 'original_score', 'cross_score']]

    global_tracker = create_global_tracker(mode, manual_hdev_pipelines)

    for pipeline_name in manual_hdev_pipelines:
        write_cross_application_header_to_log(pipeline_name)

        if mode == "mean_test" or mode == "best_test":
            # only run the pipeline on its own dataset
            # and let it raise an error
            regular_dataset = pipeline_name
            print(f"Running {pipeline_name} on {regular_dataset} ...")

            # compute the complexity of tests
            # print number of runs and time estimation
            # update time estimation after every run
            global_tracker.start_run()
            # run pipeline on dataset, but do not process cross_score
            cross_score = run_pipeline_on_dataset(
                pipeline_name,
                get_initial_state_by_pipeline_name(pipeline_name),
                regular_dataset
            )
            global_tracker.end_run()

            # Save score in list
            if type(cross_score) is not float:
                cross_scores.append([pipeline_name, 'same', cross_score, 'same'])
            else:
                cross_scores.append([pipeline_name, 'same', f"{cross_score:.4f}", 'same'])

            continue

        try:
            # Actually run the pipeline on all cross datasets
            graph = get_initial_state_by_pipeline_name(pipeline_name)

            global_tracker.start_run()
            original_score = run_pipeline_on_dataset(pipeline_name, graph)
            global_tracker.end_run()

            # pick cross-datasets minus the current
            for cross_dataset in [key for key in manual_hdev_pipelines if key != pipeline_name]:
                try:
                    global_tracker.start_run()
                    cross_score = run_pipeline_on_dataset(pipeline_name, graph, cross_dataset)
                    global_tracker.end_run()

                    write_cross_application_log(
                        pipeline_name,
                        f"{pipeline_name};{original_score};{cross_dataset};{cross_score};\n"
                    )

                    write_cross_application_log(pipeline_name,
                                                f"{pipeline_name};{original_score};{cross_dataset};{cross_score};\n")
                    # Save score in list
                    cross_scores.append([pipeline_name, cross_dataset, f"{original_score:.4f}", f"{cross_score:.4f}"])

                except Exception as e:
                    # Even failed runs took time; you probably still want to close the run.
                    global_tracker.end_run()
                    print(f"Error running cross dataset {cross_dataset} on pipeline {pipeline_name}: {e}")
                    write_cross_application_log(pipeline_name, f"ERROR: {e};\n")
                    # Save score in list
                    cross_scores.append([pipeline_name, cross_dataset, f"{original_score:.4f}", f"FAILED: {e}"])

        except Exception as e:
            print(f"Error running pipeline {pipeline_name}: {e}")
            write_cross_application_log(pipeline_name, f"FAILED: {e};\n")
            # write error to list
            cross_scores.append([pipeline_name, f"FAILED: {e}", '--', '--'])
            continue

    for idx, row in enumerate(cross_scores):
        # header
        if idx == 0:
            print("| " + " | ".join(row) + " |")
            print("|" + "|".join(" --- " for _ in row) + "|")
            continue

        # data rows
        print("| " + " | ".join(map(str, row)) + " |")


def main():
    print("CGP Pipeline Cross Application")
    print("-" * 30)
    print("1 - MEAN (by MCC) hdev pipeline cross application")
    print("2 - BEST (by MCC) hdev pipeline cross application")
    print("3 - Test MEAN (by MCC) hdev pipeline cross application (only one pipeline)")
    print("4 - Test BEST (by MCC) hdev pipeline cross application (only one pipeline)")
    print("0 - Exit")
    selection = input("Selection: ")

    # Exit program
    if selection == "0":
        print("Exiting ...")
        return 0

    # 4 -- Cross-apply cgp pipelines on all datasets (ca. 900 runs)
    if selection == "1":
        print("MEAN (by MCC) hdev pipeline cross application ...")
        manual_cross_apply_hdev_pipelines(mode="mean")

    if selection == "2":
        print("BEST (by MCC) hdev pipeline cross application ...")
        manual_cross_apply_hdev_pipelines(mode="best")
        return 0

    if selection == "3":
        print("Test MEAN (by MCC) hdev pipeline cross application ...")
        manual_cross_apply_hdev_pipelines(mode="mean_test")
        return 0

    if selection == "4":
        print("Test BEST (by MCC) hdev pipeline cross application ...")
        manual_cross_apply_hdev_pipelines(mode="best_test")
        return 0

if __name__ == "__main__":
    main()
