"""
=======================================
severstal-steel_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code
from settings import EVIAS_SRC_PATH


def get_severstal_steel_mean_pipeline(params, dataset_path=None):
    pipeline_name = "severstal-steel_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/severstal-steel/train_cgp/images"

    # Parameters
    param_lines = "<l>        MaskHeightBF := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaskWidthBF := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[3]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[4]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[5]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[6]) + "'</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * BinomialFilter</c>\n" \
                "<l>        binomial_filter(Image, Image, MaskWidthBF, MaskHeightBF)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * VarThreshold</c>\n" + \
                get_var_threshold_code() + \
                "<c></c>\n" + \
                "<c>        * Union1</c>\n" + \
                "<l>        union1(Region, Region)</l>\n" + \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


severstal_steel_mean_pipeline_initial_params = [
    17,
    5,
    29,
    23,
    0.2000001,
    13,
    'not_equal'
]

severstal_steel_bounds = [
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37],
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v) / 10.0 for v in range(-10, 10, 1)],
    [0,128],
    ['not_equal', 'light', 'equal', 'dark']
]

severstal_steel_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                    "severstal-steel", "train_cgp")
