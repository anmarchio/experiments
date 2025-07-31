"""
=======================================
MVTec_AD_Hazelnut_Crack_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, get_area_to_rectangle
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Hazelnut_Crack_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Hazelnut_Crack_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/hazelnut_crack_train/images"

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
    core_code = "<c>        * GrayClosing</c>\n" \
                "<l>        get_image_type(Image, Type)</l>\n" + \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" + \
                "<l>        gray_closing(Image, StructElement, Image)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * Apply StructElement Ellipse to Closing</c>\n" + \
                "<l>        local_threshold(Image, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, " \
                "Scale])</l>\n" + \
                "<c></c>\n" + \
                get_area_to_rectangle() + \
                "<c></c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Hazelnut_Crack_mean_pipeline_initial_params = [
    4,
    28,
    30,
    'adapted_std_deviation',
    'light',
    21,
    0.5
]

MVTec_AD_Hazelnut_Crack_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
]

MVTec_AD_Hazelnut_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "MVTecAnomalyDetection", "hazelnut_crack_train")
