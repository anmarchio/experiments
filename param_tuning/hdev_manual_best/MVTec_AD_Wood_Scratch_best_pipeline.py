"""
=======================================
MVTec_AD_Wood_Scratch_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code, \
    sobel_check_filter_type, scale_to_gray
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Wood_Scratch_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Wood_Scratch_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/wood_scratch_train/images"

    # Parameters
    param_lines = (
                "<l>        MaskType := '" + str(params[0]) + "'</l>\n"
                "<l>        MaskSizeMedian := " + str(params[1]) + "</l>\n"
                "<c></c>\n"
                "<l>        FilterType := '" + str(params[2]) + "'</l>\n"
                "<l>        MaskSizeSobel := " + str(params[3]) + "</l>\n"
                "<c></c>\n"
                "<l>        Method := '" + str(params[4]) + "'</l>\n"
                "<l>        LightDark := '" + str(params[5]) + "'</l>\n"
                "<l>        MaskSizeThresh := " + str(params[6]) + "</l>\n"
                "<l>        Scale := " + str(params[7]) + "</l>\n"
                "<c></c>\n"
                "<l>        A := " + str(params[8]) + "</l>\n"
                "<l>        B := 30</l>\n"
                "<l>        C := -0.392699</l>\n"
                "<c></c>\n"
            )

    # Core pipeline
    core_code = (
            "<c>* MedianWeighted</c>\n"
            "<l>        median_weighted(Image, ImageWeighted, MaskType, MaskSizeMedian)</l>\n"
            "<c></c>\n"
            "<c>* SobelAmp</c>\n"
            "<l>        sobel_amp(ImageWeighted, Image, FilterType, MaskSizeSobel)</l>\n"
            "<c></c>\n"
            "<c>* LocalThreshold</c>\n"
            "<c>        *access_channel(Image, Image, 1)</c>\n"
            + scale_to_gray() +
            "<l>        convert_image_type(ScaledImage, ScaledImage, 'byte')</l>\n"
            "<l>        local_threshold(ScaledImage, Region, Method, LightDark, ['mask_size','scale'], [MaskSizeThresh, Scale])</l>\n"
            "<c></c>\n"
            "<c>* Closing (Circle SE)</c>\n"
            "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n"
            "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n"
            "<l>        closing(Region, StructElement, Region)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Wood_Scratch_best_pipeline_initial_params = [
    'gauss',  # MaskType
    3,  # MaskSizeMedian
    'y',  # FilterType
    7,  # MaskSizeSobel
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSizeThresh
    0.2,  # Scale
    30  # A - only A is used
]

MVTec_AD_Wood_Scratch_best_pipeline_bounds = [

    ['inner', 'outer', 'circle', 'gauss'],  # MaskType
    [v for v in range(1, 21)],  # MaskSizeMedian
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSizeSobel
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 100, 2)],  # MaskSizeThresh
    [round(0.1 * v, 1) for v in range(1, 20)],  # Scale
    [v for v in range(1, 50)]  # A
]

MVTec_AD_Wood_Scratch_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                          "MVTecAnomalyDetection", "wood_scratch_train")
