"""
=======================================
MVTec_AD_Pultrusion_Window_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    sobel_check_filter_type, area_size_threshold, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Window_mean_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Window_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/window_cgp/train/images"

    # Parameters
    param_lines = "<l>        MinGray := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaxGray := " + str(params[1]) + "</l>\n" + \
                  "<l>        FilterType := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[3]) + "</l>\n" + \
                  "<l>        MinRatio := " + str(params[4]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[5]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[6]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * CropSmallestRetangle</c>\n" + \
                get_crop_rectangle_code() + \
                "<c>        </c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                sobel_check_filter_type() + \
                "<l>        sobel_amp(Image, Image, FilterType, MaskSize)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Crop Rectangle</c>\n" + \
                get_crop_rectangle_code()

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Window_mean_pipeline_initial_params = [
    21, # MinGray
    255, # MaxGray
    'y', # FilterType
    3, # MaskSize
    0.0399999991059303, # MinRatio
    27, # MaskHeight
    29 # MaskWidth
]

Pultrusion_Window_mean_pipeline_bounds = [
    [v for v in range(1, 255, 1)], # MinGray
    [v for v in range(1, 255, 1)], # MaxGray
    ['y', 'y_binomial', 'x', 'x_binomial'], # FilterType
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39], # MaskSize
    # [v for v in range(0.01, 1.0, 0.01)], # MinRatio
    [i / 100.0 for i in range(1, 101)], # MinRatio
    [v for v in range(1, 255, 1)], # MaskHeight
    [v for v in range(1, 255, 1)] # MaskWidth
]

Pultrusion_Window_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                      "Pultrusion", "window_cgp", "train")
