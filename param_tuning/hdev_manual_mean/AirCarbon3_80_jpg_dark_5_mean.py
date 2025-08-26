"""
=======================================
AirCarbon3_80.jpg_dark_5_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_5_mean_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_mean_5_best_pipeline"

    if dataset_path is None:
        # Default dataset path if not provided
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_5/images"

    # Parameters
    param_lines = "<l>        FilterType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[3]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[4]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[5]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[6]) + "'</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, " \
                "LightDark)</l>\n" \
                "<l>        union1(Region, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_5_mean_pipeline_initial_params = [
    'y_binomial',
    5,
    25,
    29,
    0.00000007450581,
    31,
    'dark'
]

AirCarbon3_80_jpg_dark_5_mean_pipeline_bounds = [
    ['y_binomial', 'x', 'x_binomial', 'y'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v / 10.0) for v in range(0, 10, 1)],
    [v for v in range(0, 128, 1)],
    ['dark', 'light']
]

AirCarbon3_80_jpg_dark_5_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_5")
