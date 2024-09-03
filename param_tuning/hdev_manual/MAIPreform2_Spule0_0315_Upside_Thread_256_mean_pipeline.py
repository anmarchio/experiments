"""
=======================================
MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline(params):
    pipeline_name = "MAIPreform2_Spule0-0315_Upside_Thread_256_mean_pipeline"
    dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole_256/training/images"

    # Parameters
    param_lines = "<l>        DiffusionCoefficient := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Contrast := " + str(params[1]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[2]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[3]) + "</l>\n" + \
                  "<l>        Channel := " + str(params[4]) + "</l>\n" + \
                  "<l>        Threshold := " + str(params[5]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * Anisotrophic Diffusion</c>\n" \
                "<l>        anisotropic_diffusion(Image, Image, 'weickert', 5, 1, 10)</l>\n" \
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


MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline_initial_params = [
    'perona-malik',
    2,
    1,
    100,
    1,
    4
]

MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline_bounds = [
    ['perona-malik', 'weickert', 'parabolic'],
    [2, 5, 10, 20, 50, 100],
    [0.5, 1.0, 3.0],
    [1, 3, 10, 100, 500],
    [1,2,3],
    [0,255]
]

MAIPreform2_Spule0_0315_Upside_Thread_256_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                                  "MAIPreform2.0",
                                                                                  "20170502_Compositence",
                                                                                  "Spule0-0315_Upside",
                                                                                  "undone_thread_hole_256",
                                                                                  "training")
