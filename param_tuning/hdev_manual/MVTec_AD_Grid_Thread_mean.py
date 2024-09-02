"""
=======================================
MVTec_AD_Grid_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code, \
    get_ellipse_struct_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Grid_Thread_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Grid_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/grid_thread_train/images"

    # Parameters
    param_lines = "<l>        MinGray := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaxGray := " + str(params[1]) + "</l>\n" + \
                  "<l>        MinRatio := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[4]) + "</l>\n" + \
                  "<l>        FilterType := '" + str(params[5]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[6]) + "</l>\n" + \
                  "<l>        Sigma := " + str(params[7]) + "</l>\n" + \
                  "<l>        A_1 := " + str(params[8]) + "</l>\n" + \
                  "<l>        B_1 := " + str(params[9]) + "</l>\n" + \
                  "<l>        A_2 := " + str(params[10]) + "</l>\n" + \
                  "<l>        B_2 := " + str(params[11]) + "</l>\n" + \
                  "<l>        C_2 := " + str(params[12]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * CropSmallesRectangle</c>\n" \
                "<l>        threshold(Image, Region, MinGray, MaxGray)</l>\n" + \
                "<l>        smallest_rectangle1(Region, Row1, Column1, Row2, Column2)</l>\n" + \
                "<l>        crop_rectangle1(Image, Image, Row1, Column1, Row2, Column2)</l>\n" + \
                "<c></c>\n" + \
                "<l>        copy_image(Image, Image1)</l>\n" + \
                "<l>        copy_image(Image, Image2)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * Path 1</c>\n" + \
                "<c>        * -------</c>\n" + \
                get_crop_rectangle_code() + \
                "<l>        Region1 := Region</l>\n"

    core_code += "<c></c>\n" + \
                 "<c>        * Path 2</c>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c></c>\n" + \
                 "<c>        * SobelAmp</c>\n" + \
                 "<l>        sobel_amp(Image2, Image2, FilterType, MaskSize)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * AutoThreshold</c>\n" + \
                 "<l>        abs_image(Image2, Image2)</l>\n" + \
                 "<l>        if(Type != 'byte' and Type != 'uint2' and Type != 'real')</l>\n" + \
                 "<l>            convert_image_type(Image2, Image2, 'byte')</l>\n" + \
                 "<l>        endif</l>\n" + \
                 "<l>        auto_threshold(Image2, Region2, Sigma)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * Union2 (Path 1 > Path 2)</c>\n" + \
                 "<l>        union2(Region1, Region2, Region)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * MERGE 1>2</c>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c></c>\n" + \
                 get_ellipse_struct_code(params[8], params[9], None) + \
                 "<l>        opening(Region, StructElement, Region)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * Union1</c>\n" + \
                 "<l>        union1(Region, Region)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * Closing</c>\n" + \
                 "<l>        gen_rectangle1(RectangleStructElement, 0, 0, A_2, B_2)</l>\n" + \
                 "<l>        closing(Region, RectangleStructElement, Region)</l>\n" + \
                 "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Grid_Thread_mean_pipeline_initial_params = [
    19,
    255,
    0.0399999991059303,
    13,
    19,
    'y',
    7,
    0.5,
    21,
    20,
    27,
    7,
    0.392699
]

MVTec_AD_Grid_Thread_mean_pipeline_bounds = [
    [18, 22],
    [255],
    [float(v) * 0.005 for v in range(2, 22, 1)],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [0, 0.5, 1, 2, 3, 4, 5],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)],
    [v for v in range(1, 50, 1)],
    [-1.178097, -0.785398, -0.392699, 0.0, 0.392699, 0.785398, 1.178097]
]

MVTec_AD_Grid_Thread_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                         "MVTecAnomalyDetection", "grid_thread_train")
