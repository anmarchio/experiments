"""
=======================================
CrackForest_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_CrackForest_mean_pipeline(params, dataset_path=None):
    pipeline_name = "CrackForest_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/CrackForest/small_dataset/images"

    # Parameters
    param_lines = "<l>        Method := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[2]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[3]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * LocalThreshold</c>\n" \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])  </l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CrackForest_mean_pipeline_initial_params = [
    'adapted_std_deviation',
    'dark',
    21,
    0.3
]

CrackForest_mean_pipeline_bounds = [
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
]

CrackForest_training_source_path = os.path.join(EVIAS_SRC_PATH, "CrackForest", "small_dataset")
