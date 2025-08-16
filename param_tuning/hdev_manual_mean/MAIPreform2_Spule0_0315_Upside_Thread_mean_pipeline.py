"""
=======================================
MAIPreform2_Spule0-0315_Upside_Thread_mean_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0-0315_Upside_Thread_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole/training/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        Channel := " + str(params[3]) + "</l>\n" + \
                  "<l>        Threshold := " + str(params[3]) + "</l>\n" + \
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


MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline_initial_params = [
    28,
    27,
    40,
    1,
    4
]

MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    [1, 2, 3],
    [v for v in range(0, 255, 1)],
]

MAIPreform2_Spule0_0315_Upside_Thread_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                                        "MAIPreform2.0",
                                                                                        "20170502_Compositence",
                                                                                        "Spule0-0315_Upside",
                                                                                        "undone_thread_hole",
                                                                                        "training")
