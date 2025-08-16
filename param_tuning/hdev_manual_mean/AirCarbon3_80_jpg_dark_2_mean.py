"""
=======================================
AirCarbon3_80.jpg_dark_2_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_2_mean_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_2_mean_pipeline"
    if dataset_path is None:
        # Default dataset path
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_2/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        FilterType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Min := " + str(params[1]) + "</l>\n" + \
                  "<l>        Max := " + str(params[2]) + "</l>\n" + \
                                                             "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        roberts(Image, ImageRoberts, FilterType)</l>\n" \
                "<l>        threshold(Image, Region, Min, Max)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_2_mean_pipeline_initial_params = [
    'gradient_sum',
    70,
    240
]

AirCarbon3_80_jpg_dark_2_mean_pipeline_bounds = [
    ['gradient_sum'],
    [0,255],
    [1,255]
]

AirCarbon3_80_jpg_dark_2_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_2")
