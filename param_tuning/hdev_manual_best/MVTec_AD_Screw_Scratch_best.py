"""
=======================================
MVTec_AD_Screw_Scratch_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, convert_margin_to_int, \
    get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Screw_Scratch_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Screw_Scratch_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/screw_scratch_neck_train/images"

    # Parameters
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                      "<l>        Low := " + str(params[2]) + "</l>\n" + \
                      "<l>        High := " + str(params[3]) + "</l>\n" + \
                      "<l>        NonMaximumSuppression := '" + str(params[4]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[6]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[7]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[8]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[9]) + "</l>\n" + \
                      "<l>        B := " + str(params[10]) + "</l>\n" + \
                      "<l>        C := 0</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* EdgesImage</c>\n"
            "<l>        edges_image(Image, ImageEdges, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n"
            "<c></c>\n"
            "<c>* LocalThreshold</c>\n"
            "<l>        local_threshold(ImageEdges, RegionThresh, Method, LightDark, ['mask_size','scale'], [MaskSize, Scale])</l>\n"
            "<c></c>\n"
            "<c>* Closing (Circle SE)</c>\n"
            "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n"
            "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n"
            "<l>        closing(RegionThresh, StructElement, Region)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Screw_Scratch_best_pipeline_initial_params = [
        'canny',  # Filter
        0.4,  # Alpha
        10,  # Low
        30,  # High
        'nms',  # NonMaximumSuppression
        'adapted_std_deviation',  # Method
        'dark',  # LightDark
        21,  # MaskSize
        0.2,  # Scale
        18,  # A
        7  # B
]

MVTec_AD_Screw_Scratch_best_pipeline_bounds = [
        ['canny', 'sobel_fast', 'shen', 'lanser1'],  # Filter
        [round(0.1 * v, 1) for v in range(1, 20)],  # Alpha
        [v for v in range(1, 255)],  # Low
        [v for v in range(1, 255)],  # High
        ['nms', 'inms', 'hvnms', 'none'],  # NonMaximumSuppression
        ['adapted_std_deviation', 'mean', 'max'],  # Method
        ['dark', 'light'],  # LightDark
        [v for v in range(3, 100, 2)],  # MaskSize
        [round(0.1 * v, 1) for v in range(1, 20)],  # Scale
        [v for v in range(1, 50)],  # A
        [v for v in range(1, 50)]  # B
]

MVTec_AD_Screw_Scratch_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "screw_scratch_neck_train")
