"""
=======================================
MVTec_AD_Metal_Nut_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    get_ellipse_struct_code, get_crop_rectangle_img2_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Metal_Nut_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Metal_Nut_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/metal_nut_color_train/images"

    # Parameters
    param_lines =  "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                   "<l>        Radius := " + str(params[1]) + "</l>\n" + \
                   "<l>        ModePercent := " + str(params[2]) + "</l>\n" + \
                   "<l>        Margin := '" + str(params[3]) + "'</l>\n" + \
                   "<l>        FilterType := '" + str(params[4]) + "'</l>\n" + \
                   "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                   "<l>        MaskSize2 := " + str(params[6]) + "</l>\n" + \
                   "<l>        MinRatio := " + str(params[7]) + "</l>\n" + \
                   "<l>        MaskHeight := " + str(params[8]) + "</l>\n" + \
                   "<l>        MaskWidth := " + str(params[9]) + "</l>\n" + \
                   "<l>        A := " + str(params[10]) + "</l>\n" + \
                   "<l>        B := " + str(params[11]) + "</l>\n" + \
                   "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * PATH 1</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        * DualRank</c>\n" \
                "<c>        </c>\n" \
                + convert_margin_to_int() + \
                "<l>        dual_rank(Image, Image1, MaskType, Radius, ModePercent, Margin)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * SobelAmp</c>\n" \
                "<l>        get_image_type(Image1, Type)</l>\n" \
                "<l>        if(FilterType == 'x_binomial' or FilterType == 'y_binomial')</l>\n" \
                "<l>            if(Type != 'byte' and Type != 'int2' and Type != 'real')</l>\n" \
                "<l>                convert_image_type(Image1, Image1, 'byte')</l>\n" \
                "<l>            endif</l>\n" \
                "<l>        elseif(Type != 'byte' and Type != 'int2' and Type != 'uint2' and Type != 'real')</l>\n" \
                "<l>            convert_image_type(Image1, Image1, 'byte')</l>\n" \
                "<l>        endif</l>\n" \
                "<l>        sobel_amp(Image1, Image1, FilterType, MaskSize)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * ZeroCrossing</c>\n" \
                "<c>        * ---</c>\n" \
                "<l>        zero_crossing(Image1, Region1)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * PATH 2</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        * GaussFilter</c>\n" \
                "<l>        gauss_filter(Image, Image2, MaskSize2)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * CropRectangle</c>\n" \
                + get_crop_rectangle_img2_code() + \
                "<c>        </c>\n" \
                "<c>        * Connection</c>\n" \
                "<l>        connection(Region2, Region2)</l>\n" \
                "<c>                </c>\n" \
                "<c>        * Union2</c>\n" \
                "<l>        union2(Region1, Region2, Region)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * PATH 3</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        * Opening</c>\n" \
                "<c>        </c>\n" \
                + get_ellipse_struct_code(params[9], params[10], None) + \
                "<c></c>\n" \
                "<l>        opening(Region, StructElement, Region)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Metal_Nut_mean_pipeline_initial_params = [
    'circle',
    61,
    66,
    'OneEighty',
    'x',
    3,
    3,
    0.0949999988079071,
    29,
    7,
    27,
    15
]

MVTec_AD_Metal_Nut_mean_pipeline_bounds = [
    ['circle', 'square'],#MaskType
    [1,101],# Radius
    [1,100],# ModePercent
    ['cyclic','continued','Zero','Thirty','Sixty','Ninety','OneTwenty','OneFifty','OneEighty','TwoTen','TwoForty','TwoFiftyFive'],# Margin
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [float(v) * 0.005 for v in range(2, 22, 1)],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [v for v in range(1,30,1)],
    [v for v in range(1,30,1)],
]

MVTec_AD_Metal_Nut_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "MVTecAnomalyDetection", "metal_nut_color_train")
