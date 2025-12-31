"""
=======================================
MVTec_AD_Tile_Crack_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Tile_Crack_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Tile_Crack_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/tile_crack_train/images"


    # Parameters
    param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[1]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[2]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        MaskSizeThresh := " + str(params[4]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[5]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[6]) + "</l>\n" + \
                      "<l>        B := " + str(params[7]) + "</l>\n" + \
                      "<l>        C := -1.178097</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* MedianWeighted</c>\n"
            "<l>        median_weighted(Image, ImageWMedian, MaskType, MaskSize)</l>\n"
            "<c></c>\n"
            "<c>* LocalThreshold</c>\n"
            "<l>        local_threshold(ImageWMedian, RegionThresh, Method, LightDark, ['mask_size','scale'], [MaskSizeThresh, Scale])</l>\n"
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
            "<l>        phi := 0.0</l>\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n"
            "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<l>        closing(RegionThresh, StructElement, Region)</l>\n"
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Tile_Crack_best_pipeline_initial_params = [
        'inner',  # MaskType
        3,  # MaskSizeMedian
        'adapted_std_deviation',  # Method
        'dark',  # LightDark
        21,  # MaskSizeThresh
        0.5,  # Scale
        29,  # A
        23  # B
]

MVTec_AD_Tile_Crack_best_pipeline_bounds = [
        ['inner', 'outer', 'circle', 'square'],  # MaskType
        [v for v in range(1, 21)],  # MaskSizeMedian
        ['adapted_std_deviation', 'mean', 'max'],  # Method
        ['dark', 'light'],  # LightDark
        [v for v in range(3, 100, 2)],  # MaskSizeThresh
        [round(0.1 * v, 1) for v in range(1, 20)],  # Scale
        [v for v in range(1, 50)],  # A
        [v for v in range(1, 50)]  # B
]

MVTec_AD_Tile_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "tile_crack_train")
