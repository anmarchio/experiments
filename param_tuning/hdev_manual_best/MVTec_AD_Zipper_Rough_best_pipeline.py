"""
=======================================
MVTec_AD_Zipper_Rough_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Zipper_Rough_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Zipper_Rough_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/zipper_rough_train/images"

        # Parameters
        param_lines = (
                "<l>        FilterType := '" + str(params[0]) + "'</l>\n" + \
                "<l>        MaskSize := " + str(params[1]) + "</l>\n"
                "<c></c>\n"
                "<l>        A := " + str(
                    params[2]) + "</l>\n"
                        "<l>        B := " + str(params[3]) + "</l>\n"
                        "<l>        C := 0.785398</l>\n"                                                               
                        "<c></c>\n"
                )

        # Core pipeline
        core_code = (
            "<c>* KirschAmp</c>\n"
            "<l>        kirsch_amp(Image, ImageKirsch)</l>\n"
            "<c></c>\n"
            "<c>* SobelAmp</c>\n"
            "<l>        sobel_amp(ImageKirsch, ImageAmp, FilterType, MaskSize)</l>\n"
            "<c></c>\n"
            "<c>* ZeroCrossing</c>\n"
            "<l>        zero_crossing(ImageAmp, RegionZero)</l>\n"
            "<c></c>\n"
            "<c>* Closing (Ellipse SE)</c>\n"
            "<l>        tuple_max2(A, B, max_rad)</l>\n"
            "<l>        phi := C</l>\n"
            "<l>        longer := A</l>\n"
            "<l>        shorter := B</l>\n"
            "<l>        if (shorter > longer)</l>\n"
            "<l>            tmp := shorter</l>\n"
            "<l>            shorter := longer</l>\n"
            "<l>            longer := tmp</l>\n"
            "<l>        endif</l>\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n"
            "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<l>        closing(RegionZero, StructElement, Region)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Zipper_Rough_best_pipeline_initial_params = [
    'y',  # FilterType
    7,  # MaskSize
    26,  # A
    27,  # B
    0.785398 # C
]

MVTec_AD_Zipper_Rough_best_pipeline_bounds = [
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [-1.178097, -0.785398, -0.392699, 0.0, 0.392699, 0.785398, 1.178097]  # C
]

MVTec_AD_Zipper_Rough_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                          "MVTecAnomalyDetection", "zipper_rough_train")
