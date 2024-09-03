"""
=======================================
MAIPreform2_Spule0-0315_Upside_mean_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_mean_pipeline(params):
    pipeline_name = "MAIPreform2_Spule0_0315_Upside_mean_pipeline"
    dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone/training/images"

    # Parameters
    param_lines = "<l>        FilterTypeSA := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskSizeSA := " + str(params[1]) + "</l>\n" + \
                  "<l>        Channel := " + str(params[2]) + "</l>\n" + \
                  "<l>        Threshold := " + str(params[3]) + "</l>\n" + \
                  "<l>        DiffusionCoefficient := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        Contrast := " + str(params[5]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[6]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[7]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GrayClosing</c>\n" \
                "<c>        * with struct element circle</c>\n" \
                "<c>        * StructElementType Ellipse</c>\n" \
                "<c>        * using A, B and C as shape_params</c>\n" \
                "<l>        get_image_type(Image, Type)</l>\n" \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" \
                "<l>        gray_closing(Image, StructElement, Image)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * ThresholdAccessChannel</c>\n" \
                "<c>        </c>\n" \
                "<l>        abs_image(Image, Image)</l>\n" \
                "<c>        </c>\n" \
                "<l>        count_channels(Image, NumChannels)</l>\n" \
                "<l>        if(NumChannels == 3)</l>\n" \
                "<l>           access_channel(Image, Image, Channel)</l>\n" \
                "<l>           threshold(Image, Region, Threshold, 255)</l>\n" \
                "<l>        else</l>\n" \
                "<l>            threshold(Image, Region, Threshold, 255)</l>\n" \
                "<l>        endif</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0315_Upside_mean_pipeline_initial_params = [
    'y',
    5,
    1,
    23,
    'parabolic',
    10,
    3,
    1
]

MAIPreform2_Spule0_0315_Upside_mean_pipeline_bounds = [
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['perona-malik', 'weickert', 'parabolic'],
    [2, 5, 10, 20, 50, 100],
    [0.5, 1.0, 3.0],
    [1, 3, 10, 100, 500],
    [1, 2, 3],
    [0, 255]
]

MAIPreform2_Spule0_0315_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                                 "MAIPreform2.0",
                                                                                 "20170502_Compositence",
                                                                                 "Spule0-0315_Upside",
                                                                                 "undone",
                                                                                 "training")
