import os

import numpy as np


def get_stats(img_path, lbl_path):
    if len(os.listdir(img_path)) != len(os.listdir(lbl_path)):
        print("[ERROR] Images and labels differ in amount. Aborted.")
        return []
    entropy_arr = np.array([])
    blurriness_arr = np.array([])
    brightness_arr = np.array([])
    image_size = np.array([])
    label_size = np.array([])

    label_count_per_image = np.array([])
    relative_label_size = np.array([])

    hist_entropy = np.array([])
    jpeg_complexity = np.array([])
    fractal_dimension = np.array([])
    texture_features = np.array([])
    edge_density = np.array([])
    laplacian_variance = np.array([])
    num_superpixels = np.array([])

    for i in range(len(os.listdir(img_path))):
        print("Reading: " + os.path.join(img_path, os.listdir(img_path)[i]))
        image = io.imread(os.path.join(img_path, os.listdir(img_path)[i]))

        entropy_arr = np.append(entropy_arr, [compute_image_shannon_entropy(image)])
        blurriness_arr = np.append(blurriness_arr,
                                   [compute_blurriness(image)])
        brightness_arr = np.append(brightness_arr, [image_brightness(image)])
        image_size = np.append(image_size, [get_image_size(image)])
        label_size_array = get_label_size_array(os.path.join(lbl_path, os.listdir(lbl_path)[i]))
        label_size = np.append(label_size, [label_size_array])

        label_count_per_image = np.append(label_count_per_image, [label_size[-1].size])
        relative_label_size_value = 0.0
        if label_size_array.size > 0 and label_size_array.sum() > 0:
            relative_label_size_value = (float(label_size_array.sum()) / label_size_array.size) / image_size[-1]
        relative_label_size = np.append(relative_label_size, [relative_label_size_value])

        hist_entropy = np.append(hist_entropy, [compute_histogram_entropy(image)])
        jpeg_complexity = np.append(jpeg_complexity,
                                    [compute_jpeg_complexity(os.path.join(img_path, os.listdir(img_path)[i]))])
        fractal_dimension = np.append(fractal_dimension, [compute_fractal_dimension(image)])
        texture_features = np.append(texture_features, [compute_texture_features(image)])
        edge_density = np.append(edge_density, [compute_edge_density(image)])
        laplacian_variance = np.append(laplacian_variance, [compute_laplacian_variance(image)])
        num_superpixels = np.append(num_superpixels, [count_superpixels(image)])

    return [entropy_arr,
            blurriness_arr,
            brightness_arr,
            image_size,
            label_size,
            label_count_per_image,
            relative_label_size,
            hist_entropy,
            jpeg_complexity,
            fractal_dimension,
            texture_features,
            edge_density,
            laplacian_variance,
            num_superpixels
            ]


def read_dir_to_norm_dict(read_dir_path):
    norm_arr_dict = {}
    for dir in os.path.listdir(read_dir_path):
        stats_arr = get_stats(os.path.join(read_dir_path, dir, "test"),
                              os.path.join(read_dir_path, dir, "ground_truth"))
        norm_arr_dict[dir] = [preprocessing.normalize(arr[:, np.newaxis], axis=0).ravel() for arr in stats_arr]
    return norm_arr_dict