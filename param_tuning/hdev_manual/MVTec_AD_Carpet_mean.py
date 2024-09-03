"""
=======================================
MVTec_AD_Carpet_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Carpet_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Carpet_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/carpet_train/images"

    # Parameters
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                  "<l>        Low := " + str(params[2]) + "</l>\n" + \
                  "<l>        High := " + str(params[3]) + "</l>\n" + \
                  "<l>        NonMaximumSuppression := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        FilterType := '" + str(params[5]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[6]) + "</l>\n" + \
                  "<l>        Sigma := " + str(params[7]) + "</l>\n" + \
                  "<l>        A_1 := " + str(params[8]) + "</l>\n" + \
                  "<l>        B_1 := " + str(params[9]) + "</l>\n" + \
                  "<l>        Iterations1 := " + str(params[10]) + "</l>\n" + \
                  "<l>        A_2 := " + str(params[11]) + "</l>\n" + \
                  "<l>        B_2 := " + str(params[12]) + "</l>\n" + \
                  "<l>        Iterations2 := " + str(params[13]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * EdgesImage</c>\n" \
                "<l>        edges_image(Image, Image, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                "<l>        sobel_amp(Image, Image, FilterType, MaskSize)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * AutoThreshold  </c>\n" + \
                "<l>        abs_image(Image, Image)</l>\n" + \
                "<l>        get_image_type(Image, Type)</l>\n" + \
                "<l>        if(Type != 'byte' and Type != 'uint2' and Type != 'real')</l>\n" + \
                "<l>            convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>        endif</l>\n" + \
                "<l>        auto_threshold(Image, Region, Sigma)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * Dilation1</c>\n" + \
                "<l>        tuple_ceil(A_1 + 1, param1)</l>\n" + \
                "<l>        tuple_ceil(B_1 + 1, param2)</l>\n" + \
                "<l>        gen_circle(StructElement1, param1, param2, A_1)</l>\n" + \
                "<l>        dilation1(Region, Region, StructElement1, Iterations1)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * Erosion1</c>\n" + \
                get_ellipse_struct_code(params[8], params[9], None) + \
                "<l>        erosion1(Region, Region, StructElement2, Iterations2)</l>\n" + \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Carpet_mean_pipeline_initial_params = [
    'canny',
    0.5,
    30,
    45,
    'nms',
    'y_binomial',
    7,
    0.5,
    1,
    18,
    30,
    6,
    5,
    49

]

MVTec_AD_Carpet_mean_pipeline_bounds = [
    ['canny'],
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
    [5, 10, 15, 20, 25, 30, 40],
    [5, 10, 15, 20, 25, 30, 40, 50, 60, 70],
    ['nms', 'inms', 'hvnms', 'none'],
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [0, 0.5, 1, 2, 3, 4, 5],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 50, 1)]
]

MVTec_AD_Carpet_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                    "MVTecAnomalyDetection", "carpet_train")
