"""
=======================================
MVTec_AD_Pultrusion_Resin_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code, \
    area_size_threshold, convert_margin_to_int
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Resin_best_pipeline(params, dataset_path=None):
    pipeline_name = "Pultrusion_Resin_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Pultrusion/resin_cgp/train/images"

        # Parameters
        param_lines = (
                "<l>        FilterType := '" + str(params[0]) + "'</l>\n"
                                                                "<l>        MaskSize := " + str(params[1]) + "</l>\n"
                                                                                                             "<c></c>\n"
                                                                                                             "<l>        Method := '" + str(
            params[2]) + "'</l>\n"
                         "<l>        LightDark := '" + str(params[3]) + "'</l>\n"
                                                                        "<c></c>\n"
                                                                        "<l>        Min := " + str(params[4]) + "</l>\n"
                                                                                                                "<l>        Max := " + str(
            params[5]) + "</l>\n"
                         "<l>        Features := '" + str(params[6]) + "'</l>\n"
                                                                       "<c></c>\n"
                                                                       "<l>        A := " + str(params[7]) + "</l>\n"
                                                                                                             "<l>        B := " + str(
            params[8]) + "</l>\n"
                         "<c></c>\n"
        )

        # Core pipeline
        core_code = (
            "<c>* Branch 1: SobelAmp -> ZeroCrossing -> SelectShape</c>\n"
            "<l>        sobel_amp(Image, ImageAmp, FilterType, MaskSize)</l>\n"
            "<l>        zero_crossing(ImageAmp, RegionZero)</l>\n"
            "<l>        select_shape(RegionZero, RegionShape, Features, 'and', Min, Max)</l>\n"
            "<c></c>\n"
            "<c>* Branch 2: BinaryThreshold</c>\n"
            "<l>        binary_threshold(Image, RegionBin, Method, LightDark, UsedThreshold)</l>\n"
            "<c></c>\n"
            "<c>* Merge</c>\n"
            "<l>        union2(RegionShape, RegionBin, RegionUnion)</l>\n"
            "<c></c>\n"
            "<c>* Opening (Ellipse SE)</c>\n"
            "<l>        tuple_max2(A, B, max_rad)</l>\n"
            "<l>        phi := 0.0</l>\n"
            "<l>        longer := A</l>\n"
            "<l>        shorter := B</l>\n"
            "<l>        if (shorter > longer)</l>\n"
            "<l>            tmp := shorter</l>\n"
            "<l>            shorter := longer</l>\n"
            "<l>            longer := tmp</l>\n"
            "<l>        endif</l>\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n"
            "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<l>        opening(RegionUnion, StructElement, Region)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Resin_best_pipeline_initial_params = [
    'y_binomial',  # FilterType
    7,  # MaskSize
    'max_separability',  # Method
    'light',  # LightDark
    29,  # Min
    99999,  # Max
    'outer_radius',  # Features
    16,  # A
    29  # B
]

Pultrusion_Resin_best_pipeline_bounds = [
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    ['max_separability', 'entropy', 'otsu'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(1, 500)],  # Min
    [v for v in range(500, 200000, 1000)],  # Max
    ['outer_radius', 'ra', 'roundness'],  # Features
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)]  # B
]

Pultrusion_Resin_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                     "Pultrusion", "resin_cgp", "train")
