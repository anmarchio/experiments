"""
=======================================
AirCarbon3_80.jpg_dark_5_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_5_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_5_best_pipeline"

    if dataset_path is None:
        # Default dataset path if not provided
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_5/images"

        # Parameters
        param_lines = "<l>        FilterType1 := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        MaskSize1 := " + str(params[1]) + "</l>\n" + \
                      "<l>        FilterType2 := '" + str(params[2]) + "'</l>\n" + \
                      "<l>        MaskSize2 := " + str(params[3]) + "</l>\n" + \
                      "<l>        Method := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        MaskSizeThreshold := " + str(params[6]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[7]) + "</l>\n" + \
                      "<c></c>\n"

        # Core Pipeline Code
        core_code = "<l>        sobel_amp(Image, ImageAmp1, FilterType1, MaskSize1)</l>\n" \
                    "<l>        sobel_amp(ImageAmp1, ImageAmp2, FilterType2, MaskSize2)</l>\n" \
                    "<l>        local_threshold(ImageAmp2, Region, Method, MaskSizeThreshold, LightDark, Scale)</l>\n"

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_5_best_pipeline_initial_params = [
    'y_binomial',  # FilterType1
    3,  # MaskSize1
    'y_binomial',  # FilterType2
    7,  # MaskSize2
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSizeThreshold
    0.3  # Scale
]

AirCarbon3_80_jpg_dark_5_best_pipeline_bounds = [
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'sum_abs_binomial', 'sum_sqrt_binomial', 'x_binomial', 'y_binomial'],
    # FilterType1
    [3, 5, 7, 9, 11, 13, 15],  # MaskSize1
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'sum_abs_binomial', 'sum_sqrt_binomial', 'x_binomial', 'y_binomial'],
    # FilterType2
    [3, 5, 7, 9, 11, 13, 15],  # MaskSize2
    ['adapted_std_deviation', 'max_separability', 'otsu', 'smooth_histo', 'histo'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 101, 2)],  # MaskSizeThreshold
    [round(v * 0.1, 1) for v in range(1, 20)]  # Scale
]

AirCarbon3_80_jpg_dark_5_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_5")
