"""
=======================================
MT_Blowhole_train_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MT_Blowhole_train_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MT_Blowhole_train_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/Magnetic-Tile-Defect/MT_Blowhole_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        get_image_type(Image, Type)</l>\n" \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" \
                "<l>        gray_erosion(Image, StructElement, Image)</l>\n" \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, " \
                "Scale])</l>\n "

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MT_Blowhole_train_mean_pipeline_initial_params = [
    2,
    4,
    10,
    'adapted_std_deviation',
    'dark',
    31,
    0.5
]

MT_Blowhole_train_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5],
]

MT_Blowhole_train_training_source_path = os.path.join(EVIAS_SRC_PATH, "Magnetic-Tile-Defect", "MT_Blowhole_train")
