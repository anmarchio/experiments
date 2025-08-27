"""
=========================
CF_ReferenceSet_Small_Dark_best_pipeline.py
=========================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_CF_ReferenceSet_Small_Dark_best_pipeline(params, dataset_path=None):
    pipeline_name = "CF_ReferenceSet_Small_Dark_best_pipeline"

    if dataset_path is None:
        # Default dataset path for CF_ReferenceSet_Small_Dark
        dataset_path = "/Aircarbon2/CF_ReferenceSet_Small_Dark/images"

    # Parameters
    param_lines = "<l>        FilterTypeY := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskSizeY := " + str(params[1]) + "</l>\n" + \
                  "<l>        FilterTypeX := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        MaskSizeX := " + str(params[3]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                  "<l>        MaskSizeThresh := " + str(params[6]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[7]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        sobel_amp(Image, ImageSobelY, FilterTypeY, MaskSizeY)</l>\n" \
                "<l>        sobel_amp(ImageSobelY, ImageSobelX, FilterTypeX, MaskSizeX)</l>\n" \
                "<l>        local_threshold(ImageSobelX, Region, Method, LightDark, MaskSizeThresh, Scale)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CF_ReferenceSet_Small_Dark_best_pipeline_initial_params = [
    'y',  # FilterTypeY
    5,  # MaskSizeY
    'x',  # FilterTypeX
    5,  # MaskSizeX
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSizeThresh
    0.2  # Scale
]

CF_ReferenceSet_Small_Dark_best_pipeline_bounds = [
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterTypeY
    [3, 5, 7, 9],  # MaskSizeY
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterTypeX
    [3, 5, 7, 9],  # MaskSizeX
    ['adapted_std_deviation', 'max_separability', 'otsu'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 101, 2)],  # MaskSizeThresh
    [round(v * 0.1, 1) for v in range(1, 50)]  # Scale
]

CF_ReferenceSet_Small_Dark_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2",
                                                               "CF_ReferenceSet_Small_Dark")
