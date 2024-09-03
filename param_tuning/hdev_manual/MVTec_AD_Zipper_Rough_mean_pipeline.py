"""
=======================================
MVTec_AD_Zipper_Rough_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Zipper_Rough_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Zipper_Rough_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/zipper_rough_train/images"

    # Parameters
    param_lines = "<l>        MaskSize1 := " + str(params[0]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[3]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[4]) + "</l>\n" + \
                  "<l>        A := " + str(params[5]) + "</l>\n" + \
                  "<l>        B := " + str(params[6]) + "</l>\n" + \
                  "<l>        C := " + str(params[7]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GaussFilter</c>\n" + \
                "<c>        </c>\n" + \
                "<c>       gauss_filter(Image, Image, MaskSize1)</c>\n" + \
                "<c>        </c>\n" + \
                "<c>        * LocalThreshold</c>\n" + \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])</l>\n" \
                "<c>        </c>\n" + \
                "<c>        * Closing</c>\n" \
                "<l>        gen_rectangle1(RectangleStructElement, 0, 0, A, B)</l>\n" \
                "<l>        closing(Region, RectangleStructElement, Region)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Zipper_Rough_mean_pipeline_initial_params = [
    11,
    'adapted_std_deviation',
    'dark',
    21,
    0.2,
    22,
    20,
    -0.785398
]

MVTec_AD_Zipper_Rough_mean_pipeline_bounds = [
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v) / 10.0 for v in range(-10, 10, 1)]
]

MVTec_AD_Zipper_Rough_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "zipper_rough_train")
