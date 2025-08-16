"""
=======================================
MVTec_AD_Pultrusion_Resin_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code, \
    area_size_threshold, convert_margin_to_int
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Resin_mean_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Resin_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/resin_cgp/train/images"

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
    core_code = "<c>        * CropSmallestRectangle</c>\n" + \
                convert_margin_to_int() + \
                "<l>        median_image(Image, Image, MaskType, Radius, Margin)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                "<l>        get_image_type(Image2, Type)</l>\n" + \
                "<l>        if(FilterType == 'x_binomial' or FilterType == 'y_binomial')</l>\n" + \
                "<l>            if(Type != 'byte' and Type != 'int2' and Type != 'real')</l>\n" + \
                "<l>                convert_image_type(Image2, Image2, 'byte')</l>\n" + \
                "<l>            endif</l>\n" + \
                "<l>        elseif(Type != 'byte' and Type != 'int2' and Type != 'uint2' and Type != 'real')</l>\n" + \
                "<l>            convert_image_type(Image2, Image2, 'byte')</l>\n" + \
                "<l>        endif</l>\n" + \
                "<l>        sobel_amp(Image2, Image, FilterType, MaskSize)</l>\n" + \
                "<c>        </c>\n" + \
                area_size_threshold() + \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Resin_mean_pipeline_initial_params = [
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

Pultrusion_Resin_mean_pipeline_bounds = [
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

Pultrusion_Resin_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                     "Pultrusion", "resin_cgp", "train")
