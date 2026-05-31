import os
import sys
from datetime import datetime

import cv2
import json

from pathlib import Path

import numpy as np

from complexity.metrics import rectangle_size, shannon_entr, histogram_entr, variance_of_laplacian, brightness_metric, \
    jpeg_complexity, texture_features, edge_density, number_of_superpixels, number_of_labels, blurriness_metric, \
    fractal_dimension, label_size, relative_label_size, lbl_hist_entropy, lbl_fractal_dimension, lbl_texture_features, \
    lbl_edge_density, lbl_laplacian_variance, lbl_num_superpixels
from dashboard.create_analysis_plots import compute_complexity_and_fitness_correlation
from dashboard.vars import COMPLEXITY_METRICS
from experiment_params_data import DATASETS
from settings import RESULTS_DATA_PATH, EVIAS_SRC_PATH

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def iter_images(folder):
    folder = Path(folder)

    for path in folder.rglob("*"):
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path

def get_lbl_mask_for_image(image_path):
    image_path = Path(image_path)

    label_folder = image_path.parent.parent / "labels"
    label_path = label_folder / image_path.name

    if not label_path.exists():
        label_path = label_path.with_suffix(".png")

    if not label_path.exists():
        print(f"Warning: no label mask found for {image_path.name}")
        return None

    label_mask = cv2.imread(str(label_path), cv2.IMREAD_GRAYSCALE)

    if label_mask is None:
        print(f"Warning: could not read label mask: {label_path}")
        return None

    return label_mask

def compute_metric_values_for_image(metric, image, label_mask=None):
    if metric == "entropy_arr":
        return shannon_entr(image)
    elif metric == "blurriness_arr":
        return blurriness_metric(image)
    elif metric == "brightness_arr":
        return brightness_metric(image)
    elif metric == "image_size":
        return rectangle_size(image)
    elif metric == "hist_entropy":
        return histogram_entr(image)
    elif metric == "jpeg_complexity":
        return jpeg_complexity(image)
    elif metric == "fractal_dimension":
        return fractal_dimension(image)
    elif metric == "texture_features":
        return texture_features(image)
    elif metric == "edge_density":
        return edge_density(image)
    elif metric == "laplacian_variance":
        return variance_of_laplacian(image)
    elif metric == "num_superpixels":
        return number_of_superpixels(image)

    if label_mask is None:
        return 0.0

    if metric == "label_count_per_image":
        return number_of_labels(label_mask)
    elif metric == "label_size":
        return label_size(label_mask)
    elif metric == "relative_label_size":
        return relative_label_size(label_mask)
    elif metric == "lbl_hist_entropy":
        return lbl_hist_entropy(label_mask)
    elif metric == "lbl_fractal_dimension":
        return lbl_fractal_dimension(label_mask)
    elif metric == "lbl_texture_features":
        return lbl_texture_features(label_mask)
    elif metric == "lbl_edge_density":
        return lbl_edge_density(label_mask)
    elif metric == "lbl_laplacian_variance":
        return lbl_laplacian_variance(label_mask)
    elif metric == "lbl_num_superpixels":
        return lbl_num_superpixels(label_mask)

    return None


def run_compute_complexity(
    datasets,
    output_json="complexity_metrics.json",
    base_path="."
):
    results = {}

    for ds_name, ds_info in datasets.items():

        image_folder = Path(base_path) / ds_info["train"]

        if not image_folder.exists():
            print(f"Warning: path does not exist: {image_folder}")
            continue

        print(f"Processing dataset: {ds_name}")

        # Create one list per metric
        dataset_metrics = {
            metric: [] for metric in COMPLEXITY_METRICS
        }

        for image_path in iter_images(image_folder):

            print("Processing image:", image_path)

            image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

            if image is None:
                print(f"Warning: could not read image: {image_path}")
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            label_mask = get_lbl_mask_for_image(image_path)

            # Compute all metrics for current image
            for metric in COMPLEXITY_METRICS:

                value = compute_metric_values_for_image(
                    metric,
                    image,
                    label_mask
                )

                # Handle numpy values for JSON serialization
                if isinstance(value, np.generic):
                    value = value.item()

                dataset_metrics[metric].append(value)

        # Convert dict -> ordered list
        results[ds_name] = [
            dataset_metrics[metric]
            for metric in COMPLEXITY_METRICS
        ]

        print("Processed images:", len(next(iter(dataset_metrics.values()))))
        print("=" * 30)

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
            base_path=EVIAS_SRC_PATH
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
