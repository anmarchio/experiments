"""
=======================================
AirCarbon3_80.jpg_dark_3_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_3_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_3_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_3/images"

    This is not working, yet!!
    # Parameters
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                  "<l>        NonMaximumSuppression := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        Low := " + str(params[3]) + "</l>\n" + \
                  "<l>        High := " + str(params[4]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[5]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[6]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[7]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[8]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[9]) + "'</l>\n" + \
                                                             "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        edges_image(Image, Image, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n" \
                "<l>        var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, LightDark)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_3_best_pipeline_initial_params = [
    'canny',
    1.1,
    'nms',
    25,
    45,
    13,
    7,
    0.5000001,
    5,
    'not_equal'
]

AirCarbon3_80_jpg_dark_3_best_pipeline_bounds = [
    ['canny'],
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
    ['nms', 'inms', 'hvnms', 'none'],
    [5, 10, 15, 20, 25, 30, 40],
    [5, 10, 15, 20],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v / 10.0) for v in range(0, 10, 1)],
    [v for v in range(0, 128, 1)],
    ['dark', 'equal', 'light', 'not_equal']
]

AirCarbon3_80_jpg_dark_3_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_3")
