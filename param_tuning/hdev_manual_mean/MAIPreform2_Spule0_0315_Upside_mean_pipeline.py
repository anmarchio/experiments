"""
=======================================
MAIPreform2_Spule0-0315_Upside_mean_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, scale_to_gray
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0_0315_Upside_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone/training/images"

    # Parameters
    param_lines = "<l>        FilterTypeSA := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskSizeSA := " + str(params[1]) + "</l>\n" + \
                  "<l>        DiffusionCoefficient := '" + str(params[2]) + "'</l>\n" + \
                  "<l>        Contrast := " + str(params[3]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[4]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[5]) + "</l>\n" + \
                  "<l>        Channel := " + str(params[6]) + "</l>\n" + \
                  "<l>        Threshold := " + str(params[7]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        copy_image(Image, ImageB)</l>\n" \
                "<c>        * SobelAmp</c>\n" \
                "<l>        sobel_amp(Image, Image, FilterTypeSA, MaskSizeSA)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * ZeroCrossingA</c>\n" \
                "<c>        </c>\n" + \
                "<l>        convert_image_type(Image, Image, 'int2')</l>\n" + \
                scale_to_gray() + \
                "<l>        zero_crossing(ScaledImage, RegionA)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * AnisotropicDiffusion</c>\n" \
                "<l>        anisotropic_diffusion(ImageB, ImageB, DiffusionCoefficient, Contrast, Theta, Iterations)</l>\n" \
                "<c>        </c>\n" \
                "<c>        * ThresholdAccessChannel</c>\n" \
                "<c>        </c>\n" \
                "<l>        abs_image(ImageB, ImageB)</l>\n" \
                "<c>        </c>\n" \
                "<l>        count_channels(ImageB, NumChannels)</l>\n" \
                "<l>        if(NumChannels == 3)</l>\n" \
                "<l>           access_channel(ImageB, ImageB, Channel)</l>\n" \
                "<l>           threshold(ImageB, RegionB, Threshold, 255)</l>\n" \
                "<l>        else</l>\n" \
                "<l>            threshold(ImageB, RegionB, Threshold, 255)</l>\n" \
                "<l>        endif</l>\n" \
                "<c>        </c>\n" \
                "<c>        * Union2</c>\n" \
                "<l>        union2(RegionA, RegionB, Region)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0315_Upside_mean_pipeline_initial_params = [
    'y',
    3,
    'parabolic',
    10,
    3,
    1,
    1,
    23,
]

MAIPreform2_Spule0_0315_Upside_mean_pipeline_bounds = [
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    ['perona-malik', 'weickert', 'parabolic'],
    [2, 5, 10, 20, 50, 100],
    [0.5, 1.0, 3.0],
    [v for v in range(1, 10, 1)], # actually range(1,500,1), but set to low number to reduce complexity
    [1, 2, 3],
    [0, 255],
]

MAIPreform2_Spule0_0315_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                   "MAIPreform2.0",
                                                                   "20170502_Compositence",
                                                                   "Spule0-0315_Upside",
                                                                   "undone",
                                                                   "training")
