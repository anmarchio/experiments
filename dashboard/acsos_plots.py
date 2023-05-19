import os

import numpy as np

from dashboard.acsos_vars import ACSOS_DATASET_NAMES, ACSOS_STD_DEV, ACSOS_MEANS, ACSOS_NUMBER_OF_IMAGES, \
    ACSOS_NUMBER_OF_RUNS
from dashboard.plotting import plot_fitness_per_dataset
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

    print_fitness_values_in_table(modified_dataset_names, mean_std_dev_fitness, ACSOS_NUMBER_OF_IMAGES, ACSOS_NUMBER_OF_RUNS)


def create_acsos_complexity_plot():
    pass
