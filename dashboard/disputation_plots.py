import os

from dashboard.classic_cgp_vars import CLASSIC_CGP_MEANS, CLASSIC_CGP_STD_DEV, get_harmonized_values
from dashboard.plotting import plot_fitness_per_dataset, plot_fitness_per_dataset_with_overlay, \
    wilcoxon_signed_rank_test
from dashboard.utils import print_fitness_values_in_table
from settings import WDIR


def create_fitness_overlay_plot():
    print("Reading variables ...")
    reduced_acsos_means, reduced_acsos_std_dev, modified_dataset_names = get_harmonized_values()

    basic_mean_std_dev_fitness = list(zip(reduced_acsos_means, reduced_acsos_std_dev))
    overlay_mean_std_dev_fitness = list(zip(CLASSIC_CGP_MEANS, CLASSIC_CGP_STD_DEV))

    plot_fitness_per_dataset(
        "Fitness per Dataset",
        "Fitness",
        modified_dataset_names,
        basic_mean_std_dev_fitness,
        orientation='v',
        path=os.path.join(WDIR, "scripts", "report", "fitness_per_benchmark_dataset.png"),
        show_names=True
    )

    print(f"Plot saved to {WDIR}/scripts/report/fitness_per_benchmark_dataset.png")

    plot_fitness_per_dataset_with_overlay(
        "Fitness per Dataset",
        "Fitness",
        modified_dataset_names,
        basic_mean_std_dev_fitness,
        overlay_mean_std_dev_fitness,
        orientation='v',
        path=os.path.join(WDIR, "scripts", "report", "fitness_per_dataset_overlay.png"),
        show_names=True
    )

    print(f"Plot saved to {WDIR}/scripts/report/fitness_per_dataset_overlay.png")
    
    print_fitness_values_in_table(modified_dataset_names, basic_mean_std_dev_fitness,
                                  [""]*len(basic_mean_std_dev_fitness),
                                  [""]*len(basic_mean_std_dev_fitness))
    print_fitness_values_in_table(modified_dataset_names, overlay_mean_std_dev_fitness,
                                  [""]*len(basic_mean_std_dev_fitness),
                                  [""]*len(basic_mean_std_dev_fitness))


def classic_vs_enhanced_rank_test():
    print("Reading variables ...")
    reduced_acsos_means, reduced_acsos_std_dev, modified_dataset_names = get_harmonized_values()

    wilcoxon_signed_rank_test(CLASSIC_CGP_MEANS, reduced_acsos_means)