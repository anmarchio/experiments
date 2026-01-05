"""
=======================================
MAIPreform2_Spule0-0315_Upside_Thread_best_pipeline.py
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline(params, dataset_path=None):
    pipeline_name = "MAIPreform2_Spule0-0315_Upside_Thread_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole/training/images"

    # Parameters
    param_lines = "<l>        MinRatio := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[1]) + "</l>\n" + \
                      "<l>        MaskWidth := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[3]) + "</l>\n" + \
                      "<l>        B := " + str(params[4]) + "</l>\n" + \
                      "<l>        GrayValueMax := " + str(params[5]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* CropRectangle (center crop)</c>\n"
            "<l>        get_image_size(Image, Width, Height)</l>\n"
            "<l>        Row1 := Height/2 - MaskHeight/2</l>\n"
            "<l>        Col1 := Width/2 - MaskWidth/2</l>\n"
            "<l>        Row2 := Height/2 + MaskHeight/2</l>\n"
            "<l>        Col2 := Width/2 + MaskWidth/2</l>\n"
            "<l>        crop_rectangle1(Image, ImageCrop, Row1, Col1, Row2, Col2)</l>\n"
            "<c></c>\n"
            "<c>* GrayClosing</c>\n"
            "<l>        get_image_type(ImageCrop, Type)</l>\n"
            "<l>        gen_disc_se(SE, Type, A, B, GrayValueMax)</l>\n"
            "<l>        gray_closing(ImageCrop, SE, Region)</l>\n"
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline_initial_params = [
    0.02,  # MinRatio
    7,  # MaskHeight
    29,  # MaskWidth
    12,  # A
    18,  # B
    2  # GrayValueMax
]

MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline_bounds = [
    [0.0, 0.05, 0.1],  # MinRatio (example)
    [v for v in range(1, 100)],  # MaskHeight
    [v for v in range(1, 200)],  # MaskWidth
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(0, 255)]  # GrayValueMax
]

MAIPreform2_Spule0_0315_Upside_Thread_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                                                        "MAIPreform2.0",
                                                                                        "20170502_Compositence",
                                                                                        "Spule0-0315_Upside",
                                                                                        "undone_thread_hole",
                                                                                        "training")
