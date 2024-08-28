"""
=========================
CF_ReferenceSet_Small_Dark_mean_pipeline.py
=========================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_CF_ReferenceSet_Small_Dark_mean_pipeline(params):
    pipeline_name = "CF_ReferenceSet_Small_Dark_mean_pipeline"
    dataset_path = "/Aircarbon2/CF_ReferenceSet_Small_Dark/images"

    # Parameters
    param_lines = "<l>        FilterType1 := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        FilterType2 := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[2]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        bandpass_image(Image, Image, FilterType1)</l>\n" \
                "<l>        sobel_amp(Image, Image, FilterType2, MaskSize)</l>\n" \
                "<l>        zero_crossing(Image, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CF_ReferenceSet_Small_Dark_mean_pipeline_initial_params = [
    'lines',
    'y',
    5
]

CF_ReferenceSet_Small_Dark_mean_pipeline_bounds = [
    ['lines'],
    ['y_binomial', 'x', 'x_binomial', 'y'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]
]

CF_ReferenceSet_Small_Dark_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2",
                                                               "CF_ReferenceSet_Small_Dark")
