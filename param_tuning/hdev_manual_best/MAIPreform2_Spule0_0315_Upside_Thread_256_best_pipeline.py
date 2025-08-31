"""
=======================================
MAIPreform2_Spule0_0315_Upside_Thread_256_best_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_Thread_256_best_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0-0315_Upside_Thread_256_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole_256/training/images"

        # Parameters
        param_lines = "<l>        Channel := " + str(params[0]) + "</l>\n" + \
                      "<l>        Threshold := " + str(params[1]) + "</l>\n" + \
                      "<l>        Sign := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[3]) + "</l>\n" + \
                      "<l>        B := " + str(params[4]) + "</l>\n" + \
                      "<l>        GrayValueMax := " + str(params[5]) + "</l>\n" + \
                      "<c></c>\n"

        # Core Pipeline
        core_code = (
            "<c>* ThresholdAccessChannel</c>\n"
            "<l>        abs_image(Image, ImageB)</l>\n"
            "<l>        count_channels(ImageB, NumChannels)</l>\n"
            "<l>        if (NumChannels == 3)</l>\n"
            "<l>            access_channel(ImageB, ImageB, Channel)</l>\n"
            "<l>            threshold(ImageB, RegionB, Threshold, 255)</l>\n"
            "<l>        else</l>\n"
            "<l>            threshold(ImageB, RegionB, Threshold, 255)</l>\n"
            "<l>        endif</l>\n"
            "<c></c>\n"
            "<c>* GrayClosing</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n"
            "<l>        gen_disc_se(SE, Type, A, B, GrayValueMax)</l>\n"
            "<l>        gray_closing(RegionB, SE, Region)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0315_Upside_Thread_256_best_pipeline_initial_params = [
    1,  # Channel
    41,  # Threshold
    -1,  # Sign (kept for compatibility, even if not directly used now)
    28,  # A
    27,  # B
    40  # GrayValueMax
]

MAIPreform2_Spule0_0315_Upside_Thread_256_best_pipeline_bounds = [
    [0, 1, 2, 3],  # Channel (assuming up to 4 channels)
    [v for v in range(0, 255)],  # Threshold
    [-1, 0, 1],  # Sign (even if unused here)
    [v for v in range(1, 100)],  # A
    [v for v in range(1, 100)],  # B
    [v for v in range(0, 255)]  # GrayValueMax
]

MAIPreform2_Spule0_0315_Upside_Thread_256_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                              "MAIPreform2.0",
                                                                              "20170502_Compositence",
                                                                              "Spule0-0315_Upside",
                                                                              "undone_thread_hole_256",
                                                                              "training")
