"""
============================
FabricDefectsAITEX_mean.py
============================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_FabricDefectsAITEX_mean_pipeline(params, dataset_path=None):
    pipeline_name = "FabricDefectsAITEX_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/FabricDefectsAITEX/train/images"

    # Parameters
    # 'smooth_histo', 'light', 33, 99999, 'bulkiness', 26, 29, 1.178097
    param_lines = "<l>        Method := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[1]) + "'</l>\n" + \
                  "<l>        Min := " + str(params[2]) + "</l>\n" + \
                  "<l>        Max := " + str(params[3]) + "</l>\n" + \
                  "<l>        Features := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        A := " + str(params[5]) + "</l>\n" + \
                  "<l>        B := " + str(params[6]) + "</l>\n" + \
                  "<l>        C := " + str(params[7]) + "</l>\n" + \
                  "<c></c>\n"

    core_code = "<l>        binary_threshold(Image, Region, Method, LightDark, UsedThreshold)</l>\n" + \
                "<l>        select_shape(Region, Regions, Features, 'and', Min, Max)</l>\n" + \
                "<c>        * StructElementType Ellipse</c>\n" + \
                "<c>        * using A, B and C as shape_params</c>\n" + \
                "<l>        tuple_max2(A, B, max_rad)</l>\n" + \
                "<l>        longer := A</l>\n" + \
                "<l>        shorter := B</l>\n" + \
                "<l>        if (shorter > longer)</l>\n" + \
                "<l>            tmp := shorter</l>\n" + \
                "<l>            shorter := longer</l>\n" + \
                "<l>            longer := tmp</l>\n" + \
                "<l>        endif                </l>\n" + \
                "<l>        phi := C            </l>\n" + \
                "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n" + \
                "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n" + \
                "<c>        * Apply StructElement Ellipse to Closing</c>\n" + \
                "<l>        closing(Regions, StructElement, RegionClosing)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


FabricDefectsAITEX_mean_pipeline_initial_params = [
    'smooth_histo',
    'light',
    3,
    99999,
    'bulkiness',
    26,  # A
    29,  # B
    1.178097
]

FabricDefectsAITEX_mean_pipeline_bounds = [
    ['max_separability', 'smooth_histo'],
    ['dark', 'light'],
    [1, 99999],
    [99999, 99999],
    ['area', 'width', 'height', 'compactness', 'contlength', 'convexity', 'rectangularity', 'ra', 'rb', 'anisometry',
     'bulkiness', 'outer_radius', 'inner_radius', 'inner_width', 'inner_height', 'dist_mean'],
    [1, 30],  # A
    [1, 30],  # B
    [-1.178097, -0.785398, -0.392699, 0.0, 0.392699, 0.785398, 1.178097]  # C
]

FabricDefectsAITEX_training_source_path = os.path.join(EVIAS_SRC_PATH, "FabricDefectsAITEX",
                                                       "train")
