"""
=======================================
MVTec_AD_Wood_Scratch_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code, \
    sobel_check_filter_type
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Wood_Scratch_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Wood_Scratch_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/wood_scratch_train/images"

    # Parameters
    param_lines = "<l>        MaskSize1 := " + str(params[0]) + "</l>\n" + \
                  "<l>        FilterType := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        MaskSize2 := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[4]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[5]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[6]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[7]) + "'</l>\n" + \
                  "<l>        A := " + str(params[8]) + "</l>\n" + \
                  "<l>        B := " + str(params[9]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[10]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GaussFilter</c>\n" + \
                "<c>        </c>\n" + \
                "<c>       gauss_filter(Image, Image, MaskSize1)</c>\n" + \
                "<c>        </c>\n" + \
                get_var_threshold_code() + \
                "<c>        </c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                sobel_check_filter_type() + \
                "<l>        sobel_amp(Image, Image, FilterType, MaskSize2)</l>\n" \
                "<c>        </c>\n" + \
                get_var_threshold_code() + \
                "<c>        * Dilation</c>\n" \
                "<l>        gen_rectangle1(RectangleStructElement, 0, 0, A, B)</l>\n" \
                "<l>        dilation1(Region, RectangleStructElement, Region, Iterations) </l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Wood_Scratch_mean_pipeline_initial_params = [
    9,
    'y',
    7,
    7,
    19,
    0.1000001,
    26,
    'dark',
    4,
    3,
    14
]

MVTec_AD_Wood_Scratch_mean_pipeline_bounds = [
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v) / 10.0 for v in range(-10, 10, 1)],
    [0, 128],
    ['not_equal', 'light', 'equal', 'dark'],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)]
]

MVTec_AD_Wood_Scratch_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "wood_scratch_train")
