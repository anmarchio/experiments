"""
=========================
CF_ReferenceSet_Small_Light_mean_pipeline.py
=========================
"""
import os

from param_tuning.hdev_manual_best.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_CF_ReferenceSet_Small_Light_best_pipeline(params, dataset_path=None):
    pipeline_name = "CF_ReferenceSet_Small_Light_best_pipeline"

    if dataset_path is None:
        # Default dataset path for CF_ReferenceSet_Small_Light
        dataset_path = "/Aircarbon2/CF_ReferenceSet_Small_Light/images"

        # Parameters
        param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        MaskSizeMedian := " + str(params[1]) + "</l>\n" + \
                      "<l>        FilterType := '" + str(params[2]) + "'</l>\n" + \
                      "<l>        MaskSizeSobel := " + str(params[3]) + "</l>\n" + \
                      "<l>        Method := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        MaskSizeThresh := " + str(params[6]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[7]) + "</l>\n" + \
                      "<l>        A := " + str(params[8]) + "</l>\n" + \
                      "<l>        B := " + str(params[9]) + "</l>\n" + \
                      "<l>        C := 0.785398</l>\n" + \
                      "<c></c>\n"

        # Core Pipeline Code
        core_code = "<l>        median_weighted(Image, ImageMedian, MaskType, MaskSizeMedian)</l>\n" \
                    "<l>        sobel_amp(ImageMedian, ImageSobel, FilterType, MaskSizeSobel)</l>\n" \
                    "<l>        local_threshold(ImageSobel, Region, Method, LightDark, MaskSizeThresh, Scale)</l>\n" \
                    "<c>* Closing</c>" \
                    "<l>        tuple_ceil(A + 1, shape_param0_ceil)</l>\n" \
                    "<l>        gen_circle(StructElement, shape_param0_ceil, shape_param0_ceil, A)</l>\n" \
                    "<l>        closing(Region, StructElement, Region)</l>\n\n"

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CF_ReferenceSet_Small_Light_best_pipeline_initial_params = [
    'inner',  # MaskType
    3,  # MaskSizeMedian
    'y',  # FilterType
    5,  # MaskSizeSobel
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSizeThresh
    0.2,  # Scale
    21,  # A
    25  # B
]

CF_ReferenceSet_Small_Light_best_pipeline_bounds = [
    ['inner', 'outer'],  # MaskType
    [3, 5, 7, 9],  # MaskSizeMedian
    ['x', 'y', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9],  # MaskSizeSobel
    ['adapted_std_deviation', 'max_separability', 'otsu'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 101, 2)],  # MaskSizeThresh
    [round(v * 0.1, 1) for v in range(1, 50)],  # Scale
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
]

CF_ReferenceSet_Small_Light_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2",
                                                               "CF_ReferenceSet_Small_Light")
