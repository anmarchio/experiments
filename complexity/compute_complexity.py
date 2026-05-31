import os
import sys
from datetime import datetime

import cv2
import json

from pathlib import Path
from complexity.metrics import rectangle_size, shannon_entr, histogram_entr, variance_of_laplacian, brightness_metric, \
    jpeg_complexity, texture_features, edge_density, number_of_superpixels, number_of_labels
from dashboard.create_analysis_plots import compute_complexity_and_fitness_correlation
from experiment_params_data import DATASETS
from settings import RESULTS_DATA_PATH


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def iter_images(folder):
    folder = Path(folder)

    for path in folder.rglob("*"):
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def compute_metrics_for_image(image, label_mask=None):
    metrics = {
        "rectangle_size": rectangle_size(image),
        "shannon_entropy": shannon_entr(image),
        "histogram_entropy": histogram_entr(image),
        "variance_of_laplacian": variance_of_laplacian(image),
        "brightness": brightness_metric(image),
        "jpeg_complexity": jpeg_complexity(image),
        "texture_features": texture_features(image),
        "edge_density": edge_density(image),
        "number_of_superpixels": number_of_superpixels(image),
    }

    if label_mask is not None:
        metrics["number_of_labels"] = number_of_labels(label_mask)

    return metrics


def run_compute_complexity(
    datasets,
    output_json="complexity_metrics.json",
    base_path="."
):
    results = {}

    for dataset_group in datasets:
        for dataset_name, dataset_info in dataset_group.items():

            results[dataset_name] = {
                "publisher": dataset_info.get("publisher"),
                "train": {},
                "test": {}
            }

            for split in ["train", "test"]:
                image_folder = Path(base_path) / dataset_info[split]

                if not image_folder.exists():
                    print(f"Warning: path does not exist: {image_folder}")
                    continue

                for image_path in iter_images(image_folder):
                    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

                    if image is None:
                        print(f"Warning: could not read image: {image_path}")
                        continue

                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    metrics = compute_metrics_for_image(image)

                    results[dataset_name][split][image_path.name] = metrics

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results


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

        results = run_compute_complexity(
            datasets=DATASETS,
            output_json=output_json,
            base_path="."
        )

        print("\nFinished computing complexity metrics.")
        print(f"Output file: {output_json}")
        print(f"Datasets processed: {len(results)}")

    elif selection == "2":
        # Plot complexity / fitness correlation
        files = [
            f for f in os.listdir(RESULTS_DATA_PATH)
            if f.endswith(".json")
        ]

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
