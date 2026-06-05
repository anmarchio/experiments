import os
import sys
from datetime import datetime

from complexity.compute_complexity import perform_complexity_computation
from dashboard.create_analysis_plots import compute_complexity_and_fitness_correlation
from experiment_params_data import DATASETS
from settings import RESULTS_DATA_PATH, EVIAS_SRC_PATH


def main():
    print("=" * 30)
    print("COMPLEXITY ANALYSIS")
    print("=" * 30)
    print("[1] Compute complexity metrics")
    print("[2] Plot complexity / fitness correlation")
    print("[0] Exit")

    selection = input("Selection: ").strip()

    if selection == "1":
        current_date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        output_json = os.path.join(
            RESULTS_DATA_PATH,
            f"{current_date_time}_complexity_values.json"
        )

        results = perform_complexity_computation(
            datasets=DATASETS,
            output_json=output_json,
            base_path=EVIAS_SRC_PATH
        )

        print("\nFinished computing complexity metrics.")
        print(f"Output file: {output_json}")
        print(f"Datasets processed: {len(results)}")

    elif selection == "2":
        # Plot complexity / fitness correlation
        files = sorted(
            [
                f for f in os.listdir(RESULTS_DATA_PATH)
                if f.endswith("_complexity_values.json")
            ],
            reverse=True
        )

        if not files:
            print("ERROR: No JSON files found.")
            return 0

        print("\nSelect complexity values file")
        print("-" * 30)

        for i, filename in enumerate(files):
            print(f"[{i}] {filename}")

        file_selection = input("File: ").strip()

        if not file_selection.isdigit():
            print("ERROR: Invalid selection. Aborted.")
            return 0

        file_index = int(file_selection)

        if not 0 <= file_index < len(files):
            print("ERROR: Invalid selection. Aborted.")
            return 0

        complexity_values_json = os.path.join(RESULTS_DATA_PATH, files[int(file_selection)])

        print(f"\nSelected file: {complexity_values_json}")

        if not os.path.exists(complexity_values_json):
            print("ERROR: File does not exist. Aborted.")
            return 0

        compute_complexity_and_fitness_correlation(complexity_values_json)

    elif selection == "0":
        print("Exiting.")
        return 0

    else:
        print("ERROR: Invalid menu selection.")
        return 0

    print("Done.")
    return 0


if __name__ == "__main__":
    main()
    sys.exit()
