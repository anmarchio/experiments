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
                      "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        LightDark ':= " + str(params[4]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A2 := " + str(params[5]) + "</l>\n" + \
                      "<l>        B2 := " + str(params[6]) + "</l>\n" + \
                      "<l>        C := 0.785398</l>\n" + \
                      "<c></c>\n"

    # Core Pipeline
    core_code = "<c>* GrayOpening</c>\n" \
            "<c>* using A, B and C as shape_params</c>\n" \
            "<l>get_image_type(Image, Type)</l>\n" \
            "<l>gen_disc_se(StructElement, Type, A1, B1, GrayValueMax1)</l>\n" \
            "<l>gray_opening(Image, StructElement, Image)</l>\n" \
            "\n" \
            "<c>* BinaryThreshold</c>\n" \
            "<l>binary_threshold(Image, Region, Method, LightDark, UsedThreshold)</l>\n" \
            "\n" \
            "<c>* Closing</c>\n" \
            "<c>* StructElementType Ellipse</c>\n" \
            "<c>* using A, B and C as shape_params</c>\n" \
            "<l>tuple_max2(A2, B2, max_rad)</l>\n" \
            "<l>longer := A</l>\n" \
            "<l>shorter := B</l>\n" \
            "<l>if (shorter > longer)</l>\n" \
            "<l>    tmp := shorter</l>\n" \
            "<l>    shorter := longer</l>\n" \
            "<l>    longer := tmp</l>\n" \
            "<l>endif</l>\n" \
            "<l>phi := C2</l>\n" \
            "<l>tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n" \
            "<l>gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n" \
            "<c>* Apply StructElement Ellipse to Closing</c>\n" \
            "<l>closing(Region, StructElement, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


# Initial Parameters
MAIPreform2_Spule0_0315_Upside_best_pipeline_initial_params = [
    4, 3, 2,  # GrayOpening (A1, B1, GrayValueMax1)
    'max_separability', 'light',  # Threshold (Method, LightDark)
    26, 26  # Closing (A2, B2)
]

# Bounds for Evolutionary Search
MAIPreform2_Spule0_0315_Upside_best_pipeline_bounds = [
        [v for v in range(1, 100)],  # A1
        [v for v in range(1, 100)],  # B1
        [v for v in range(0, 255)],  # GrayValueMax1
        ['max_separability','smooth_histo'],  # Min
        ['light','dark'],  # Max
        [v for v in range(1, 100)],  # A2
        [v for v in range(1, 100)]  # B2
]

MAIPreform2_Spule0_0315_Upside_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                   "MAIPreform2.0",
                                                                   "20170502_Compositence",
                                                                   "Spule0-0315_Upside",
                                                                   "undone",
                                                                   "training")
