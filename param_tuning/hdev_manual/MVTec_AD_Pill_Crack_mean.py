"""
=======================================
MVTec_AD_Pill_Crack_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    get_ellipse_struct_code, get_crop_rectangle_img2_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Pill_Crack_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Pill_Crack_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/pill_crack_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        MinRatio := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[4]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[5]) + "</l>\n" + \
                  "<l>        A_2 := " + str(params[6]) + "</l>\n" + \
                  "<l>        B_2 := " + str(params[7]) + "</l>\n" + \
                  "<l>        C_2 := " + str(params[8]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * PATH 1</c>\n" \
                "<c>        * ------</c>\n" \
                "<c>        * DualRank</c>\n" \
                "<c>        * GrayOpening</c>\n" \
                "<c>        </c>\n" \
                "<c>        * with struct element circle</c>\n" \
                "<c>        * using A, B and C as shape_params</c>\n" \
                "<l>        get_image_type(Image, Type)</l>\n" \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" \
                "<l>        gray_opening(Image, StructElement, Image)</l>\n" \
                "c>        </c>\n" \
                "<c>        * CropRectangle</c>\n" \
                + get_crop_rectangle_code() + \
                "<c>        </c>\n" \
                "<c>        </c>\n" \
                "<c>        * Closing</c>\n" \
                "<c>        </c>\n" \
                "<c>        * with struct element circle</c>\n" \
                "<l>        tuple_ceil(A_2 + 1, shape_param0_ceil)</l>\n" \
                "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A_2)</l>\n" \
                "<c></c>\n" \
                "<l>        closing(Image, StructElement, Region)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Pill_Crack_mean_pipeline_initial_params = [
    17,
    10,
    10,
    0.109999999403954,
    29,
    29,
    9,
    20,
    -1.178097
]

MVTec_AD_Pill_Crack_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    [float(v) * 0.005 for v in range(2, 22, 1)], # MinRatio
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29], # Width
    [3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 27, 29], # Height
    [v for v in range(1, 50, 1)],
    [v for v in range(1, 50, 1)],
    [-1.178097, -0.785398, -0.392699, 0.0, 0.392699, 0.785398, 1.178097]
]

MVTec_AD_Pill_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "pill_crack_train")
