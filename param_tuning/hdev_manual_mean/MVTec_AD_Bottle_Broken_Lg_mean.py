"""
=======================================
MVTec_AD_Bottle_Broken_Lg_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Bottle_Broken_Lg_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Bottle_Broken_Lg_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/bottle_broken_large_train/images"

    # Parameters
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                  "<l>        MinRatio := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[4]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * SmoothImage</c>\n" \
                "<l>        smooth_image(Image, ImageSmooth, 'deriche2', 0.5)</l>\n" + get_crop_rectangle_code()

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Bottle_Broken_Lg_mean_pipeline_initial_params = [
    'gauss',
    47.1181,
    0.0199999995529652,
    7,
    7
]

MVTec_AD_Bottle_Broken_Lg_mean_pipeline_bounds = [
    ['deriche1', 'deriche2', 'gauss', 'shen'],
    [float(v) / 100.0 for v in range(1, 5000, 1)],
    [float(v) * 0.005 for v in range(2, 22, 1)],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29]
]

MVTec_AD_Bottle_Broken_Lg_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                              "MVTecAnomalyDetection", "bottle_broken_large_train")
