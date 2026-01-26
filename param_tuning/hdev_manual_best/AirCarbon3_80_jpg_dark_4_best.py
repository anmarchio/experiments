"""
=======================================
AirCarbon3_80.jpg_dark_4_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_AirCarbon3_80_jpg_dark_4_best_pipeline(params, dataset_path=None):
    pipeline_name = "AirCarbon3_80.jpg_dark_4_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_4/images"

    # Parameters
    param_lines = "<l>        MinGray := " + str(params[0]) + "</l>\n" + \
                  "<l>        MaxGrayOffset := " + str(params[1]) + "</l>\n" + \
                  "<l>        MinSize := " + str(params[2]) + "</l>\n" + \
                  "<l>        A := " + str(params[3]) + "</l>\n" + \
                  "<l>        B := " + str(params[4]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[5]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c></c>\n" \
                "<c>        * GrayDilation with Disc SE</c>\n" \
                "<l>        get_image_type(Image, Type)</l>\n" \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" \
                "<l>        gray_dilation(Image, StructElement, Image)</l>\n" \
                "<c></c>\n" \
                "<c>        * Fast Threshold</c>\n" \
                "<l>        fast_threshold(Image, Region, MinGray, MaxGrayOffset, MinSize)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon3_80_jpg_dark_4_best_pipeline_initial_params = [
    157,   # MinGray
    255,   # MaxGrayOffset
    124,   # MinSize
    2,     # A
    18,    # B
    20     # GrayValueMax
]

AirCarbon3_80_jpg_dark_4_best_pipeline_bounds = [
    [v for v in range(1, 255, 1)],  # MinGray
    [v for v in range(1, 255, 1)],  # MaxGrayOffset
    [v for v in range(1, 500, 1)],  # MinSize
    [v for v in range(1, 30, 1)],  # A
    [v for v in range(1, 50, 1)],  # B
    [v for v in range(1, 255, 1)]  # GrayValueMax
]

AirCarbon3_80_jpg_dark_4_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon3", "20210325_13h25_rov",
                                                             "training", "80.jpg_dark_4")
