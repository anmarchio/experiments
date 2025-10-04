"""
=======================================
MVTec_AD_Carpet_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Carpet_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Carpet_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/carpet_train/images"

    # Parameters
    param_lines = "<l>        MaskSizeGauss := " + str(params[0]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Min := " + str(params[1]) + "</l>\n" + \
                      "<l>        Max := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        FilterType := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        MaskSizeSobel := " + str(params[4]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[6]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[7]) + "</l>\n" + \
                      "<l>        B := " + str(params[8]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = "<c>* Branch 1: Threshold → GaussFilter</c>\n" + \
            "<l>        gauss_filter(Image, ImageGauss, MaskSizeGauss)</l>\n" + \
            "<l>        threshold(ImageGauss, RegionThresh, Min, Max)</l>\n" + \
            "<c></c>\n" + \
            "<c>* Branch 2: BinaryThreshold → SobelAmp</c>\n" + \
            "<l>        sobel_amp(Image, ImageAmp, FilterType, MaskSizeSobel)</l>\n" + \
            "<l>        abs_image(ImageAmp, ImageAbs)</l>\n" + \
            "<l>        convert_image_type(ImageAbs, ImageConverted, 'byte')</l>\n" + \
            "<l>        binary_threshold(ImageConverted, RegionBinary, Method, LightDark, UsedThreshold)</l>\n" + \
            "<c></c>\n" + \
            "<c>* Merge</c>\n" + \
            "<l>        union2(RegionThresh, RegionBinary, Region)</l>\n" + \
            "<c></c>\n" + \
            "<c>* Opening</c>\n" + \
            "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n" + \
            "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n" + \
            "<l>        opening(Region, StructElement, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Carpet_best_pipeline_initial_params = [
    3,  # MaskSizeGauss
    50,  # Min
    220,  # Max
    'x',  # FilterType
    3,  # MaskSizeSobel
    'smooth_histo',  # Method
    'light',  # LightDark
    16,  # A
    13  # B
]

MVTec_AD_Carpet_best_pipeline_bounds = [
    [3, 5, 7, 9],  # MaskSizeGauss
    [v for v in range(0, 255)],  # Min
    [v for v in range(0, 255)],  # Max
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9],  # MaskSizeSobel
    ['smooth_histo', 'max_separability', 'otsu'],  # Method
    ['light', 'dark'],  # LightDark
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)]  # B
]

MVTec_AD_Carpet_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                    "MVTecAnomalyDetection", "carpet_train")
