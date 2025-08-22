"""
============================
AirCarbon3_80_jpg_bright_mean.py
============================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_bright_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_bright_mean_pipeline"
    if dataset_path is None:
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_bright/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        Method := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        MaskSizeLT := " + str(params[2]) + "</l>\n" + \
                  "<l>        Scale := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        FilterTypeSA := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskSizeSA := " + str(params[5]) + "</l>\n" + \
                  "<l>        Sigma := '" + str(params[6]) + "'</l>\n" + \
                  "<l>        Rho := " + str(params[7]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[8]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[9]) + "</l>\n\n"

    # Core Pipeline Code
    core_code = "<l>        coherence_enhancing_diff (Image, Image, Sigma, Rho, Theta, Iterations)</l>\n" \
                "<c></c>\n" \
                "<l>        sobel_amp(Image, ImageAmp, FilterTypeSA, MaskSizeSA)</l>\n" + \
                "<c></c>\n" \
                "<l>        access_channel(ImageAmp, ImageAmp, 1)</l>\n" + \
                "<l>        convert_image_type(ImageAmp, ImageAmp, 'byte')</l>\n" + \
                "<l>        local_threshold(ImageAmp, Region, Method, LightDark, ['mask_size', 'scale'], " \
                "[MaskSizeLT, Scale])</l>\n" + \
                "<c></c>\n" \
                "<l>        connection(Region, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_bright_mean_pipeline_initial_params = [
    'adapted_std_deviation',
    'dark',
    15,
    0.3,
    'y_binomial',
    7,
    0.1,
    2,
    0.1,
    328,
    5,
    'adapted_std_deviation',
    'dark',
    15,
    0.2
]

AirCarbon3_80_jpg_bright_best_pipeline_bounds = [
    ['adapted_std_deviation'],
    ['light', 'dark'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
    ['y_binomial', 'x', 'x_binomial', 'y'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [0.0, 0.1, 0.5, 1.0],
    [0.0, 1.0, 3.0, 5.0, 10.0, 30.0]
    [0.1, 0.2, 0.3, 0.4, 0.5],
    [v for v in range(1, 500, 1)]
]

AirCarbon3_80_jpg_bright_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_bright")
