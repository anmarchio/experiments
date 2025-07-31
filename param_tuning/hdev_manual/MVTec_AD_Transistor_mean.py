"""
=======================================
Transistor_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Transistor_mean_pipeline(params, dataset_path = None):
    pipeline_name = "MVTec_AD_Transistor_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/transistor_damaged_case_train/images"

    # Parameters
    param_lines = "<l>        MinRatio := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[2]) + "</l>\n" + \
                  "<l>        RasterHeight := " + str(params[3]) + "</l>\n" + \
                  "<l>        RasterWidth := " + str(params[4]) + "</l>\n" + \
                  "<l>        Tolerance := " + str(params[5]) + "</l>\n" + \
                  "<l>        MinRegionSize := " + str(params[6]) + "</l>\n" + \
                  "<l>        A := " + str(params[7]) + "</l>\n" + \
                  "<l>        B := " + str(params[8]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = ("<c>        * -------</c>\n" + \
                 "<c>        * Path 1</c>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c>        * EquHistoimage</c>\n" \
                 "<l>        equ_histo_image(Image, Image)</l>\n" + \
                 get_crop_rectangle_code() + \
                 "<c></c>\n" + \
                 "<l>        Region1 := Region</l>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c>        * Path 2</c>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c>        * RegionGrowing</c>\n" + \
                 "<l>        regiongrowing(Image, Region2, RasterHeight, RasterWidth, Tolerance, MinRegionSize)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * Union2 (Path 1 > Path 2)</c>\n" + \
                 "<l>        union1(Region2, Region2)</l>\n" + \
                 "<l>        union2(Region1, Region2, Region)</l>\n" + \
                 "<c></c>\n" + \
                 "<c>        * MERGE 1>2</c>\n" + \
                 "<c>        * -------</c>\n" + \
                 "<c></c>\n" + \
                 "<l>        tuple_ceil(A + 1, param1)</l>\n" + \
                 "<l>        tuple_ceil(A + 1, param2)</l>\n" + \
                 "<l>        gen_circle(StructElement1, param1, param2, B)</l>\n" + \
                 "<l>        opening(Region, StructElement1, Region)</l>\n" + \
                 "<c></c>\n")

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Transistor_mean_pipeline_initial_params = [
    0.044999998062849,
    19,
    7,
    9,
    11,
    3,
    200,
    20,
    28
]

MVTec_AD_Transistor_mean_pipeline_bounds = [
    [float(v) * 0.005 for v in range(2, 23, 1)],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29],
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 12, 13, 18, 25],
    [1, 5, 10, 20, 50, 100, 200, 500, 1000],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)]
]

MVTec_AD_Transistor_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "transistor_damaged_case_train")
