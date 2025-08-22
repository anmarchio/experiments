"""
AirCarbon2_t_8_jpg_best.py
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def AirCarbon2_t_8_jpg_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon2_t_8.jpg_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon2/Blende5_6_1800mA_rov/training/t_8.jpg/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        MinGray := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaxGray := " + str(params[1]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[2]) + "</l>\n\n"
    # Core Pipeline Code
    core_code = "<l>        fast_threshold(Image, Region, MinGray, MaxGray, MinSize)</l>\n" \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)

AirCarbon2_t_8_jpg_best_pipeline_initial_params = [
    75,
    215,
    168
]

AirCarbon2_t_8_jpg_best_pipeline_bounds = [
    [v for v in range(1, 255, 1)],
    [v for v in range(1, 255, 1)],
    [v for v in range(2, 200, 1)]
]

AirCarbon2_t_8_jpg_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2", "Blende5_6_1800mA_rov",
                                                       "training", "t_8.jpg")