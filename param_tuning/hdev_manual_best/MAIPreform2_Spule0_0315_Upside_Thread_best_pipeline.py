"""
=======================================
MAIPreform2_Spule0-0315_Upside_Thread_best_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0-0315_Upside_Thread_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole/training/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                      "<l>        B := " + str(params[1]) + "</l>\n" + \
                      "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        MinRatio := " + str(params[3]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[4]) + "</l>\n" + \
                      "<l>        MaskWidth := " + str(params[5]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* GrayClosing</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n"
            "<l>        gen_disc_se(SE, Type, A, B, GrayValueMax)</l>\n"
            "<l>        gray_closing(Image, SE, Region)</l>\n"
            "<c></c>\n"
            "<c>* CropRectangle (center crop)</c>\n"
            + get_crop_rectangle_code()
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline_initial_params = [
    12,  # A
    18,  # B
    2,  # GrayValueMax
    0.02,  # MinRatio
    7,  # MaskHeight
    29  # MaskWidth
]

MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(0, 255)],  # GrayValueMax
    [0.0, 0.05, 0.1],  # MinRatio (example)
    [v for v in range(1, 100)],  # MaskHeight
    [v for v in range(1, 200)]  # MaskWidth
]

MAIPreform2_Spule0_0315_Upside_Thread_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                                        "MAIPreform2.0",
                                                                                        "20170502_Compositence",
                                                                                        "Spule0-0315_Upside",
                                                                                        "undone_thread_hole",
                                                                                        "training")
