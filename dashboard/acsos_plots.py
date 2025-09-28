import os
from datetime import datetime

import numpy as np

from dashboard.acsos_vars import ACSOS_DATASET_NAMES, ACSOS_STD_DEV, ACSOS_MEANS, ACSOS_NUMBER_OF_IMAGES, \
    ACSOS_NUMBER_OF_RUNS, IMG_HIST_ENTROPY_VALUES, LBL_EDGE_DENSITY_VALUES
from dashboard.plotting import plot_fitness_per_dataset, create_complexity_plot
from dashboard.utils import print_fitness_values_in_table


def create_fitness_plot():
    mean_std_dev_fitness = list(zip(ACSOS_MEANS, ACSOS_STD_DEV))
    modified_dataset_names = [[i] + [x] for i, x in enumerate(ACSOS_DATASET_NAMES)]

    plot_fitness_per_dataset(
        "Fitness per Dataset",
        "Fitness",
        modified_dataset_names,
        mean_std_dev_fitness,
        orientation='v',
        path=os.path.join("scripts", "report", "fitness_per_dataset.png"),
        show_names=True
    )

    print("Plot saved to scripts/report/fitness_per_dataset.png")

    print_fitness_values_in_table(modified_dataset_names, mean_std_dev_fitness, ACSOS_NUMBER_OF_IMAGES, ACSOS_NUMBER_OF_RUNS)


def create_acsos_complexity_plot():
    create_complexity_plot(
        "Mean Image JPEG Complexity per Dataset",
        "JPEG Complexity",
        ACSOS_DATASET_NAMES,
        IMG_HIST_ENTROPY_VALUES,
        path=os.path.join("out", "plots",
                          datetime.now().strftime('%Y%m%d-%H%M%S') +
                          "jpeg_complexity_bplot.png")
    )

    create_complexity_plot(
        "Mean Label Edge Density per Dataset",
        "Edge Density",
        ACSOS_DATASET_NAMES,
        LBL_EDGE_DENSITY_VALUES,
        path=os.path.join("out", "plots",
                          datetime.now().strftime('%Y%m%d-%H%M%S') +
                          "lbl_edge_density_bplot.png")
    )
