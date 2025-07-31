"""
=======================================
MAIPreform2_Spule0-0315_Upside_mean_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0816_Upside_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0_0816_Upside_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule2-0816_Upside/undone/durchlauf1/training/images"

    # Parameters
    param_lines = "<l>        MinRatio := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[2]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = get_crop_rectangle_code() + \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0816_Upside_mean_pipeline_initial_params = [
    0.0899999961256981,
    3,
    15
]

MAIPreform2_Spule0_0816_Upside_mean_pipeline_bounds = [
    [float(v) * 0.005 for v in range(2, 22, 1)],  # MinRatio
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],  # Width
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29]  # Height
]

MAIPreform2_Spule0_0816_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                   "MAIPreform2.0",
                                                                   "20170502_Compositence",
                                                                   "Spule2-0816_Upside",
                                                                   "undone",
                                                                   "durchlauf1",
                                                                   "training")
