"""
=======================================
MVTec_AD_Carpet_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Carpet_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Carpet_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/carpet_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                      "<l>        B := " + str(params[1]) + "</l>\n" + \
                      "<l>        GrayValMax := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Sigma := " + str(params[3]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A2 := " + str(params[4]) + "</l>\n" + \
                      "<l>        B2 := " + str(params[5]) + "</l>\n" + \
                      "<l>        GrayValMax2 := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        FilterType := '" + str(params[7]) + "'</l>\n" + \
                      "<l>        MaskSizeSobel := " + str(params[8]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Min := " + str(params[9]) + "</l>\n" + \
                      "<l>        Max := " + str(params[10]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A3 := " + str(params[11]) + "</l>\n" + \
                      "<l>        B3 := " + str(params[12]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = "<c>* Branch 1: Threshold → GaussFilter</c>\n" + \
            "<c></c>\n" + \
            "<l>        gen_disc_se(SE, 'byte', A, B, GrayValMax)</l>\n" + \
            "<c></c>\n" + \
            "<l>        gray_erosion(Image, SE, ImageErosion)</l>\n" + \
            "<c></c>\n" + \
            "<l>        auto_threshold(ImageErosion, AutoThreshRegion, Sigma)</l>\n" + \
            "<c></c>\n" + \
            "<l>        connection(AutoThreshRegion, ConnectedRegions)</l>\n" + \
            "<l>        union1(ConnectedRegions, UnionRegion)</l>\n" + \
            "<c></c>\n" + \
            "<c>* Branch 2: BinaryThreshold → SobelAmp</c>\n" + \
            "<l>        gen_disc_se(SE, 'byte', A2, B2, GrayValMax2)</l>\n" + \
            "<c></c>\n" + \
            "<l>        gray_erosion(Image, SE, ImageErosion)</l>\n" + \
            "<c></c>\n" + \
            "<l>        sobel_amp(Image, ImageAmp, FilterType, MaskSizeSobel)</l>\n" + \
            "<l>        abs_image(ImageAmp, ImageAbs)</l>\n" + \
            "<c></c>\n" + \
            "<l>        threshold(ImageAbs, ThreshRegion, Min, Max)</l>\n" + \
            "<c></c>\n" + \
            "<l>        ExpandIter := 1</l>\n" + \
            "<l>        ExpandThresh := 5</l>\n" + \
            "<c></c>\n" + \
            "<l>        gen_empty_obj(Tmp)</l>\n" + \
            "<l>        if(ExpandIter > 0)</l>\n" + \
            "<l>           expand_gray(ThreshRegion, ImageAbs, Tmp, RegionExpand, ExpandIter, 'image', ExpandThresh)</l>\n" + \
            "<l>        else</l>\n" + \
            "<l>           expand_gray(ThreshRegion, ImageAbs, Tmp, RegionExpand, ExpandIter, 'maximal', ExpandThresh)</l>\n" + \
            "<l>        endif</l>\n" + \
            "<c></c>\n" + \
            "<c>        * Merge</c>\n" + \
            "<l>        union2(ConnectedRegions, RegionExpand, Region)</l>\n" + \
            "<c></c>\n" + \
            "<l>        dev_display(Region)</l>\n" + \
            "<c></c>\n" + \
            "<c>        * Opening</c>\n" + \
            "<l>        gen_rectangle1(StructRect, 0, 0, A3, B3)</l>\n" + \
            "<l>        opening(Region, StructRect, Region)</l>\n" + \
            "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Carpet_best_pipeline_initial_params = [
    18,  # A
    3,  # B
    40,  # GrayValMax
    2,  # Sigma
    15,  # A2
    20,  # B2
    2, # GrayValMax2
    'x',  # FilterType
    7,  # MaskSizeSobel
    30,  # Min
    225,  # Max
    27, # A3
    10 # B3
]

MVTec_AD_Carpet_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    40, # GrayValMax
    [2,3,5,7,9,11,13,15],  # Sigma
    [v for v in range(1, 50)],  # A2
    [v for v in range(1, 50)],  # B2
    2,
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9],  # MaskSizeSobel
    [v for v in range(0, 255)],  # Min
    [v for v in range(0, 255)],  # Max
    [v for v in range(1, 50)],  # A3
    [v for v in range(1, 50)]  # B3
]

MVTec_AD_Carpet_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                    "MVTecAnomalyDetection", "carpet_train")
