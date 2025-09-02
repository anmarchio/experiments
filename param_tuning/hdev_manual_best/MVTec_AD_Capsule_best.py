"""
=======================================
MVTec_AD_Capsule_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Capsule_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Capsule_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/capsule_crack_train/images"

        # Parameters
        param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                      "<l>        Low := " + str(params[2]) + "</l>\n" + \
                      "<l>        High := " + str(params[3]) + "</l>\n" + \
                      "<l>        NonMaximumSuppression := '" + str(params[4]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        FilterType := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        MaskWidth := " + str(params[7]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[8]) + "</l>\n" + \
                      "<l>        StdDevScale := " + str(params[9]) + "</l>\n" + \
                      "<l>        AbsThreshold := " + str(params[10]) + "</l>\n" + \
                      "<l>        LightDark := '" + str(params[11]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[12]) + "</l>\n" + \
                      "<l>        B := " + str(params[13]) + "</l>\n" + \
                      "<l>        C := 0.392699</l>\n" + \
                      "<c></c>\n"

        # Core pipeline
        core_code = (
            "<l>        edges_image(Image, ImageEdges, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n"
            "<l>        sobel_amp(ImageEdges, ImageAmp, FilterType, MaskSize)</l>\n"
            "<c>        * VarThreshold</c>\n"
            + get_var_threshold_code() +
            "<l>        gen_circle(RectangleStructElement, 0, 0, A)</l>\n"
            "<c>        </c>\n"
            "<c>        * Closing</c>\n"
            "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n"
            "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n"
            "<l>        closing(Region, StructElement, Region)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Capsule_best_pipeline_initial_params = [
    'canny',  # Filter
    1.3,  # Alpha
    10,  # Low
    25,  # High
    'nms',  # NonMaximumSuppression
    'x',  # FilterType
    5,  # MaskSize
    9,  # MaskWidth
    17,  # MaskHeight
    0.9,  # StdDevScale
    81,  # AbsThreshold
    'light',  # LightDark
    26,  # A
    18  # B
]

MVTec_AD_Capsule_best_pipeline_bounds = [
    ['canny', 'deriche1', 'deriche2', 'sobel_fast'],  # Filter
    [round(0.1 * v, 1) for v in range(1, 30)],  # Alpha
    [v for v in range(1, 255)],  # Low
    [v for v in range(1, 255)],  # High
    ['nms', 'inms', 'hvnms', 'none'],  # NonMaximumSuppression
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9],  # MaskSize
    [v for v in range(3, 50, 2)],  # MaskWidth
    [v for v in range(3, 50, 2)],  # MaskHeight
    [round(0.1 * v, 1) for v in range(1, 20)],  # StdDevScale
    [v for v in range(1, 255)],  # AbsThreshold
    ['light', 'dark'],  # LightDark
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)]  # B
]

MVTec_AD_Capsule_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                     "MVTecAnomalyDetection", "capsule_crack_train")
