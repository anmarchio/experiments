"""
=======================================
MVTec_AD_Toothbrush_Sm_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Toothbrush_Sm_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Toothbrush_Sm_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/toothbrush_small_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        Min := " + str(params[3]) + "</l>\n" + \
                  "<l>        Max := " + str(params[4]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GrayClosing</c>\n" + \
                "<c>        </c>\n" + \
                "<c>        * with struct element circle</c>\n" + \
                "<c>        * StructElementType Ellipse</c>\n" + \
                "<c>        * using A, B and C as shape_params</c>\n" + \
                "<l>        get_image_type(Image, Type)</l>\n" \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" \
                "<l>        gray_closing(Image, StructElement, Image)</l>\n" \
                "<c>        </c>\n" + \
                "<c>        * LocalThreshold</c>\n" \
                "<l>        threshold(Image, Region, Min, Max)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Toothbrush_Sm_mean_pipeline_initial_params = [
    16,
    13,
    0,
    30,
    250
]

MVTec_AD_Toothbrush_Sm_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    [v for v in range(0, 14, 1)],
    [v for v in range(40, 51, 1)]
]

MVTec_AD_Toothbrush_Sm_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "toothbrush_small_train")
