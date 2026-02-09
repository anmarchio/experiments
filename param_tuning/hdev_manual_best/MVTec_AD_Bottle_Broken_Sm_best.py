"""
=======================================
MVTec_AD_Bottle_Broken_Sm_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_ellipse_struct_code, \
    scale_to_gray
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Bottle_Broken_Sm_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Bottle_Broken_Sm_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/bottle_broken_small_train/images"

    # Parameters
    param_lines = "<l>        MinGray := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaxGray := " + str(params[1]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        FilterType := '" + str(params[2]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[3]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Iterations := " + str(params[4]) + "</l>\n" + \
                      "<l>        A := " + str(params[5]) + "</l>\n" + \
                      "<l>        B := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>        * CropSmallestRectangle</c>\n"
            "<l>        threshold(Image, RegionRect, MinGray, MaxGray)</l>\n"
            "<l>        smallest_rectangle1(RegionRect, Row1, Column1, Row2, Column2)</l>\n"
            "<l>        crop_rectangle1(Image, ImageCrop, Row1, Column1, Row2, Column2)</l>\n"
            "<c></c>\n"
            "<l>        sobel_amp(ImageCrop, Image, FilterType, MaskSize)</l>\n"
            + scale_to_gray() +
            "<c></c>\n"
            "<l>        convert_image_type(ImageScaled, ImageAmp, 'int2')</l>\n"
            "<l>        zero_crossing(Image, RegionZero)</l>\n"
            "<c></c>\n"
            "<c>        * StructElementType Ellipse using A, B</c>\n"
            "<l>        tuple_max2(A, B, max_rad)</l>\n"
            "<l>        longer := A</l>\n"
            "<l>        shorter := B</l>\n"
            "<l>        if (shorter > longer)</l>\n"
            "<l>            tmp := shorter</l>\n"
            "<l>            shorter := longer</l>\n"
            "<l>            longer := tmp</l>\n"
            "<l>        endif</l>\n"
            "<l>        phi := 0.0</l>\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n"
            "<l>        gen_ellipse(SE, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<c></c>\n"
            "<c>        * Apply StructElement Ellipse to Dilation1</c>\n"
            "<l>        dilation1(RegionZero, SE, RegionDilation, Iterations)</l>\n"
            "<c></c>\n"
            "<l>        union1(RegionDilation, Region)</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Bottle_Broken_Sm_best_pipeline_initial_params = [
    21,  # MinGray
    255,  # MaxGray
    'y_binomial',  # FilterType
    7,  # MaskSize
    12,  # Iterations
    7.0,  # A
    3.0  # B
]

MVTec_AD_Bottle_Broken_Sm_best_pipeline_bounds = [
    [v for v in range(0, 255)],  # MinGray
    [v for v in range(0, 255)],  # MaxGray
    ['sum_abs', 'sum_sqrt', 'x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11, 13, 15],  # MaskSize
    [v for v in range(1, 50)],  # Iterations
    [float(v) for v in range(1, 50)],  # A
    [float(v) for v in range(1, 50)]  # B
]

MVTec_AD_Bottle_Broken_Sm_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                              "MVTecAnomalyDetection", "bottle_broken_small_train")
