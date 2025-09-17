"""
=======================================
AirCarbon3_80.jpg_dark_2_best_pipeline
=======================================
"""
import os

import numpy as np

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_2_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_2_best_pipeline"
    if dataset_path is None:
        # Default dataset path
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_2/images"

    # Parameters
    param_lines = "<l>        FilterTypeSA_1 := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaxSizeSA_1 := " + str(params[1]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[4]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[5]) + "</l>\n" + \
                  "<l>        Filter := '" + str(params[6]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[7]) + "</l>\n" + \
                  "<l>        NonMaximumSuppression := '" + str(params[8]) + "'</l>\n" + \
                  "<l>        Low := " + str(params[9]) + "</l>\n" + \
                  "<l>        High := " + str(params[10]) + "</l>\n" + \
                  "<l>        FilterTpyeSA_2 := '" + str(params[11]) + "'</l>\n" + \
                  "<l>        MaxSizeSA_2 := " + str(params[12]) + "</l>\n" + \
                  "<l>        Sigma := " + str(params[13]) + "</l>\n" + \
                  "<l>        A := " + str(params[14]) + "</l>\n" + \
                  "<l>        B := " + str(params[15]) + "</l>\n" + \
                  "<l>        C := 1.178097</l>\n" + \
                                                             "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>* Branch 1</c>"\
                "<l>        sobel_amp(Image, ImageAmp, FilterTypeSA_1, MaxSizeSA_1)</l>\n" \
                "<c></c>" \
                "<l>        access_channel(ImageAmp, ImageAmp, 1)</l>\n" \
                "<l>        convert_image_type(ImageAmp, ImageAmp, 'byte')</l>\n" \
                "<l>        local_threshold(ImageAmp, RegionA, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])</l>\n" \
                "<c>* Branch 2</c>" \
                "<l>        edges_image(Image, ImageAmp2, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n" \
                "<l>        sobel_amp(ImageAmp2, ImageAmp2, FilterTpyeSA_2 , MaxSizeSA_2)</l>\n" \
                "<c></c>" \
                "<c>* Merge: Histo To Thresh</c>" \
                "<l>        union1(RegionA, Region)</l>\n" \
                "<c></c>" \
                "<l>        gray_histo(Region, ImageAmp2, AbsHisto, RelativeHisto)</l>\n" \
                "<l>        histo_to_thresh(AbsHisto, Sigma, MinThresh, MaxThresh)</l>\n" \
                "<l>        threshold(ImageAmp2, Region, MinThresh, MaxThresh)</l>\n" \
                "<c></c>" \
                "<c>* Closing</c>" \
                "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n" \
                "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n" \
                "<l>        closing(Region, StructElement, Region)</l>\n\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_2_best_pipeline_initial_params = [
    'x_binomial',
    5,
    'adapted_std_deviation',
    'dark',
    15,
    0.3,
    'canny',
    1.3,
    'nms',
    25,
    45,
    'x_binomial',
    7,
    1,
    14,
    9
]

AirCarbon3_80_jpg_dark_2_best_pipeline_bounds = [
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'sum_abs_binomial', 'sum_sqrt_binomial', 'x_binomial', 'y_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5],
    ['canny', 'deriche1', 'deriche1_int4', 'deriche2', 'deriche2_int4', 'lanser1', 'lanser2', 'mshen', 'shen', 'sobel_fast'],
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.1],
    ['nms', 'hvnms', 'inms', 'none'],
    [v for v in range(1, 255, 1)],
    [v for v in range(1, 255, 1)],
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'sum_abs_binomial', 'sum_sqrt_binomial', 'x_binomial', 'y_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [np.arange(0.5, 30.0, 0.5)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)]
]

AirCarbon3_80_jpg_dark_2_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_2")
