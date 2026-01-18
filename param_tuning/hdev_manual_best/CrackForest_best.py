"""
=======================================
CrackForest_best_pipeline

THIS IS JUST A LAZY COPY FROM CrackForest_mean.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_CrackForest_best_pipeline(params, dataset_path=None):
    pipeline_name = "CrackForest_best_pipeline"

    if dataset_path is None:
        dataset_path = "/CrackForest/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<c></c>\n" + \
                  "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GrayOpening</c>\n" \
                "<l>        gen_disc_se(SE, 'byte', A, B, GrayValueMax)</l>\n" \
                "<l>        gray_opening(Image, SE, Image)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * LocalThreshold</c>\n" \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])  </l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CrackForest_best_pipeline_initial_params = [
    30,
    11,
    30,
    'adapted_std_deviation',
    'dark',
    21,
    0.3
]

CrackForest_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(0, 255)],  # GrayValueMax
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
]

CrackForest_training_source_path = os.path.join(EVIAS_SRC_PATH, "CrackForest")
