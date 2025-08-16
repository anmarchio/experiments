"""
=======================================
MVTec_AD_Pultrusion_Window_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    sobel_check_filter_type, area_size_threshold
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Window_mean_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Window_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/window_cgp/train/images"

    # Parameters
    param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Radius := " + str(params[1]) + "</l>\n" + \
                  "<l>        Margin := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        FilterType := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[4]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[5]) + "</l>\n" + \
                  "<l>        MaxSize := " + str(params[6]) + "</l>\n" + \
                  "<l>        WindowWidth := " + str(params[7]) + "</l>\n" + \
                  "<l>        WindowHeight := " + str(params[8]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * MedianImage</c>\n" + \
                convert_margin_to_int() + \
                "<l>        get_image_size(Image, Width2, Height2)</l>\n" + \
                "<l>        Width2 := Width2 / 2</l>\n" + \
                "<l>        Height2 := Height2 / 2</l>\n" + \
                "<l>        if(Width2 >= Radius)</l>\n" + \
                "<l>            radius := Radius</l>\n" + \
                "<l>        else</l>\n" + \
                "<l>            radius := Height2 - 1</l>\n" + \
                "<l>        endif</l>\n" + \
                "<c>        </c>\n" + \
                "<l>        median_image(Image, Image, MaskType, radius, Margin)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                sobel_check_filter_type() + \
                "<l>        sobel_amp(Image, Image, FilterType, MaskSize)</l>\n" + \
                "<c>        </c>\n" + \
                area_size_threshold()

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Window_mean_pipeline_initial_params = [
    'circle',
    47,
    'TwoTen',
    'y',
    7,
    10000,
    21000,
    200,
    220
]

Pultrusion_Window_mean_pipeline_bounds = [
    ['circle', 'square'],  # MaskType
    [1, 101],  # Radius
    ['cyclic', 'continued', 'Zero', 'Thirty', 'Sixty', 'Ninety', 'OneTwenty', 'OneFifty', 'OneEighty', 'TwoTen',
     'TwoForty', 'TwoFiftyFive'],  # Margin
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [v for v in range(9000, 10999, 1000)],
    [v for v in range(18000, 21999, 1000)],
    [v for v in range(160, 320, 10)],
    [v for v in range(160, 320, 10)]
]

Pultrusion_Window_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                      "Pultrusion", "window_cgp", "train")
