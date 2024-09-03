"""
=======================================
MVTec_AD_Bottle_Broken_Sm_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Bottle_Broken_Sm_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Bottle_Broken_Sm_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/bottle_broken_small_train/images"

    # Parameters
    param_lines = "<l>        FilterType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MinGray := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaxGrayOffset := " + str(params[2]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[3]) + "</l>\n" + \
                  "<l>        A := " + str(params[4]) + "</l>\n" + \
                  "<l>        B := " + str(params[5]) + "</l>\n" + \
                  "<l>        C := " + str(params[6]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * Roberts</c>\n" \
                "<l>        roberts(Image, Image, FilterType)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * FastThreshold</c>\n" + \
                "<l>        fast_threshold(Image, Region, MinGray, MaxGrayOffset, MinSize)</l>\n" + \
                "<c></c>\n" + \
                "<l>        * Closing</l>\n"

    core_code += get_ellipse_struct_code(params[4], params[5], params[6])

    core_code += "<l>        * Connection</l>\n" + \
                 "<l>        connection(Region, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Bottle_Broken_Sm_mean_pipeline_initial_params = [
    'gradient_max',
    68,
    90,
    180,
    12,
    27,
    0.0
]

MVTec_AD_Bottle_Broken_Sm_mean_pipeline_bounds = [
    ['gradient_max', 'gradient_sum', 'roberts_max'],
    [0, 254],
    [0, 255],
    [2, 200],
    [1, 30],
    [1, 30],
    [-1.178097, -0.785398, -0.392699, 0.0, 0.392699, 0.785398, 1.178097]
]

MVTec_AD_Bottle_Broken_Sm_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                              "MVTecAnomalyDetection", "bottle_broken_small_train")
