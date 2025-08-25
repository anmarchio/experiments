"""
=======================================
AirCarbon3_80.jpg_dark_1_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_1_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_1_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_1/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                  "<l>        NonMaximumSuppression := '" + str(params[2]) + "'</l>\n" \
                  "<l>        Low := " + str(params[3]) + "</l>\n" + \
                  "<l>        High := " + str(params[4]) + "</l>\n" \
                  "<c></c>\n" \ 
                  "<l>        FilterTypeSA := '" + str(params[5]) + "'</l>\n" \
                  "<l>        MaskSizeSA := " + str(params[6]) + "</l>\n" \
                  "<c></c>\n" \ 
                  "<l>        Channel := " + str(params[7]) + "</l>\n" \
                  "<l>        Threshold := " + str(params[8]) + "</l>\n" \
                  "<c></c>\n" \ 
                  "<l>        A := " + str(params[9]) + "</l>\n" \
                  "<l>        B := " + str(params[10]) + "</l>\n" \
                  "<l>        C := -1.178097</l>\n" \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>edges_image(Image, ImaAmp, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n" \
                "<c></c>\n" \
                "<l>sobel_amp(Image, ImageAmp, FilterTypeSA, MaskSizeSA)</l>\n" + \
                "<c></c>\n" \
                "<c>* ThresholdAccessChannel</c>\n" \
                "<l>abs_image(Image, Image)</l>\n" + \
                "<c></c>\n" \
                "<l>count_channels(Image, NumChannels)\n" + \
                "<l>if(NumChannels == 3)</l>\n" \
                "<l>   access_channel(Image, Image, Channel)</l>\n" \
                "<l>   threshold(Image, Region, Threshold, 255)</l>\n" \
                "<l>else</l>\n" \
                "<l>    threshold(Image, Region, Threshold, 255)</l>\n" \
                "<l>endif</l>\n" \
                "<c></c>\n" \
                "<c>* Closing</c>\n" \
                "<l>tuple_ceil(A + 1, shape_param0_ceil)</l>\n" \
                "<l>gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n" \
                "<l>closing(Region, StructElement, Region)</l>\n" \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_1_best_pipeline_initial_params = [
    'canny',
    0.8,
    30,
    45,
    'nms'
    'x',
    5,
    1,
    49,
    11,
    12
]

AirCarbon3_80_jpg_dark_1_best_pipeline_bounds = [
    ['canny', 'deriche1', 'deriche1_int4', 'deriche2', 'deriche2_int4', 'lanser1', 'lanser2', 'mshen', 'shen', 'sobel_fast'],
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.1],
    [v for v in range(1, 255, 1)],
    [v for v in range(1, 255, 1)],
    ['nms', 'hvnms', 'inms', 'none'],
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'sum_abs_binomial', 'sum_sqrt_binomial', 'x_binomial', 'y_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [1,2,3],
    [v for v in range (1,255,1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)]
]

AirCarbon3_80_jpg_dark_1_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_1")
