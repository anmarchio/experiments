"""
=======================================
MVTec_AD_Tile_Crack_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Tile_Crack_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Tile_Crack_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/tile_crack_train/images"

    # Parameters
    param_lines = "<l>        MaskHeight := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[1]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[4]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[5]) + "</l>\n" + \
                  "<l>        A := " + str(params[6]) + "</l>\n" + \
                  "<l>        B := " + str(params[7]) + "</l>\n" + \
                  "<l>        Iterations1 := " + str(params[8]) + "</l>\n" + \
                  "<l>        A_2 := " + str(params[9]) + "</l>\n" + \
                  "<l>        B_2 := " + str(params[10]) + "</l>\n" + \
                  "<l>        Iterations2 := " + str(params[11]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * BinomialFilter</c>\n" + \
                "<l>        binomial_filter(Image, Image, MaskHeight, MaskWidth)</l>\n" \
                "<c>        </c>\n" + \
                "<c>        * LocalThreshold</c>\n" \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, " \
                "Scale])</l>\n" \
                "<c>        </c>\n" \
                "<c>        * Dilation1</c>\n" \
                "<l>        gen_rectangle1(RectangleStructElement, 0, 0, A, B)</l>\n" \
                "<l>        dilation1(Region, RectangleStructElement, Region, Iterations1)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * Erosion1</c>\n" \
                "<l>        gen_rectangle1(RectangleStructElement2, 0, 0, A_2, B_2)</l>\n" \
                "<l>        erosion1(Region, RectangleStructElement2, Region, Iterations2)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Tile_Crack_mean_pipeline_initial_params = [
    19,
    17,
    'adapted_std_deviation',
    'light',
    21,
    0.3,
    20,
    9,
    4,
    23,
    14,
    3
]

MVTec_AD_Tile_Crack_mean_pipeline_bounds = [
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37],
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)]
]

MVTec_AD_Tile_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "tile_crack_train")
