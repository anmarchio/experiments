"""
============================
AirCarbon3_80_jpg_bright_mean.py
============================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_bright_mean_pipeline(params):
    pipeline_name = "AirCarbon3_80.jpg_bright_mean_pipeline"
    dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_bright/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        FilterTypeBP := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        FilterTypeSA := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        MaskSizeSA := " + str(params[2]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskSizeLT := " + str(params[5]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[6]) + "</l>\n\n"

    # Core Pipeline Code
    core_code = "<l>        bandpass_image(Image, Image, FilterTypeBP)</l>\n" \
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
    'lines',
    'y',
    5,
    'adapted_std_deviation',
    'dark',
    15,
    0.2
]

AirCarbon3_80_jpg_bright_mean_pipeline_bounds = [
    ['lines'],
    ['y_binomial', 'x', 'x_binomial', 'y'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['adapted_std_deviation'],
    ['light', 'dark'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
]

AirCarbon3_80_jpg_bright_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_bright")
