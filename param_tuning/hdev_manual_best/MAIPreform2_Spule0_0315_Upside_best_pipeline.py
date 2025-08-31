"""
=======================================
MAIPreform2_Spule0-0315_Upside_best_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_best_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0_0315_Upside_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone/training/images"

        # Parameters
        param_lines = "<l>        A1 := " + str(params[0]) + "</l>\n" + \
                      "<l>        B1 := " + str(params[1]) + "</l>\n" + \
                      "<l>        GrayValueMax1 := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Min := " + str(params[3]) + "</l>\n" + \
                      "<l>        Max := " + str(params[4]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A2 := " + str(params[5]) + "</l>\n" + \
                      "<l>        B2 := " + str(params[6]) + "</l>\n" + \
                      "<l>        GrayValueMax2 := " + str(params[7]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A3 := " + str(params[8]) + "</l>\n" + \
                      "<l>        B3 := " + str(params[9]) + "</l>\n" + \
                      "<c></c>\n"

        # Core Pipeline
        core_code = "<c>* Branch 1: GrayClosing -> Threshold</c>\n" \
                    "<l>        get_image_type(Image, Type1)</l>\n" \
                    "<l>        gen_disc_se(SE1, Type1, A1, B1, GrayValueMax1)</l>\n" \
                    "<l>        gray_closing(Image, SE1, ImageClosing)</l>\n" \
                    "<l>        threshold(ImageClosing, Region1, Min, Max)</l>\n" \
                    "<c></c>\n" \
                    "<c>* Branch 2: GrayDilation -> ZeroCrossing</c>\n" \
                    "<l>        get_image_type(Image, Type2)</l>\n" \
                    "<l>        gen_disc_se(SE2, Type2, A2, B2, GrayValueMax2)</l>\n" \
                    "<l>        gray_dilation(Image, SE2, ImageDilation)</l>\n" \
                    "<l>        zero_crossing(ImageDilation, Region2)</l>\n" \
                    "<c></c>\n" \
                    "<c>* Merge</c>\n" \
                    "<l>        union2(Region1, Region2, Region)</l>\n" \
                    "<c></c>\n" \
                    "<c>* Opening</c>\n" \
                    "<l>        opening_rectangle1(Region, Region, A3, B3)</l>\n"

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


# Initial Parameters
MAIPreform2_Spule0_0315_Upside_best_pipeline_initial_params = [
    11, 25, 5,  # GrayClosing (A1, B1, GrayValueMax1)
    10, 200,  # Threshold (Min, Max)
    4, 12, 10,  # GrayDilation (A2, B2, GrayValueMax2)
    26, 21  # Opening (A3, B3)
]

# Bounds for Evolutionary Search
MAIPreform2_Spule0_0315_Upside_best_pipeline_bounds = [
        [v for v in range(1, 100)],  # A1
        [v for v in range(1, 100)],  # B1
        [v for v in range(0, 255)],  # GrayValueMax1
        [v for v in range(0, 255)],  # Min
        [v for v in range(0, 255)],  # Max
        [v for v in range(1, 100)],  # A2
        [v for v in range(1, 100)],  # B2
        [v for v in range(0, 255)],  # GrayValueMax2
        [v for v in range(1, 100)],  # A3
        [v for v in range(1, 100)]  # B3
]

MAIPreform2_Spule0_0315_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                   "MAIPreform2.0",
                                                                   "20170502_Compositence",
                                                                   "Spule0-0315_Upside",
                                                                   "undone",
                                                                   "training")
