"""
=======================================
AirCarbon3_80.jpg_dark_4_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_4_mean_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_4_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_4/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        MaskWidth := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskHeight := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        Gap := " + str(params[2]) + "</l>\n" + \
                  "<l>        Mode := " + str(params[3]) + "</l>\n" + \
                  "<l>        MinGray := " + str(params[4]) + "</l>\n" + \
                  "<l>        MaxGrayOffset := " + str(params[5]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[6]) + "</l>\n" + \
                                                             "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        eliminate_min_max(Image, Image, MaskWidth, MaskHeight, Gap, Mode)</l>\n" \
                "<l>        fast_threshold(Image, Region, MinGray, MaxGrayOffset, MinSize)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_4_mean_pipeline_initial_params = [
    19,
    9,
    12,
    1,
    121,
    185,
    161
]

AirCarbon3_80_jpg_dark_4_mean_pipeline_bounds = [
    [float(v) for v in range(3, 31, 2)],
    [float(v) for v in range(3, 31, 2)],
    [float(v) for v in range(1, 40, 1)],
    [1.0, 2.0, 3.0],
    [1, 40],
    [1.0, 2.0, 3.0],
    [2, 200]
]

AirCarbon3_80_jpg_dark_4_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_4")
