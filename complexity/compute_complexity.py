import json
from pathlib import Path

import cv2
import numpy as np

from complexity.metrics import rectangle_size, shannon_entr, histogram_entr, variance_of_laplacian, brightness_metric, \
    jpeg_complexity, texture_features, edge_density, number_of_superpixels, number_of_labels, blurriness_metric, \
    fractal_dimension, label_size, relative_label_size, lbl_hist_entropy, lbl_fractal_dimension, lbl_texture_features, \
    lbl_edge_density, lbl_laplacian_variance, lbl_num_superpixels
from dashboard.vars import COMPLEXITY_METRICS

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def iter_images(folder):
    folder = Path(folder)

    for path in folder.rglob("*"):
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        parts_lower = [p.lower() for p in path.parts]

        if "labels" in parts_lower or "label" in parts_lower or "masks" in parts_lower or "mask" in parts_lower:
            continue

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
        return np.nan

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


def perform_complexity_computation(
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

        # Store raw per-image metric values.
        # Dataset-level aggregation and global normalization are done later
        # in compute_complexity_and_fitness_correlation().

        #results[ds_name] = [ # OLD way to store image
        #    dataset_metrics[metric]
        #    for metric in COMPLEXITY_METRICS
        #]
        results[ds_name] = {
            metric: dataset_metrics[metric] # new way: dict
            for metric in COMPLEXITY_METRICS
        }

        print("Processed images:", len(next(iter(dataset_metrics.values()))))
        print("=" * 30)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results

