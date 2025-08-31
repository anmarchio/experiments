"""
============================
FabricDefectsAITEX_best.py
============================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_FabricDefectsAITEX_best_pipeline(params, dataset_path=None):
    pipeline_name = "FabricDefectsAITEX_best_pipeline"

    if dataset_path is None:
        dataset_path = "/FabricDefectsAITEX/train/images"

        # Parameters
        param_lines = "<l>        MaskWidthEMM := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskHeightEMM := " + str(params[1]) + "</l>\n" + \
                      "<l>        Gap := " + str(params[2]) + "</l>\n" + \
                      "<l>        Mode := " + str(params[3]) + "</l>\n" + \
                      "<l>        MaskWidthVT := " + str(params[4]) + "</l>\n" + \
                      "<l>        MaskHeightVT := " + str(params[5]) + "</l>\n" + \
                      "<l>        StdDevScale := " + str(params[6]) + "</l>\n" + \
                      "<l>        AbsThreshold := " + str(params[7]) + "</l>\n" + \
                      "<l>        LightDark := '" + str(params[8]) + "'</l>\n" + \
                      "<c></c>\n"

        # Core Pipeline Code
        core_code = "<l>        eliminate_min_max(Image, ReducedImage, MaskWidthEMM, MaskHeightEMM, Gap, Mode)</l>\n" \
                    "<l>        var_threshold(ReducedImage, Region, MaskWidthVT, MaskHeightVT, StdDevScale, AbsThreshold, LightDark)</l>\n"

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


FabricDefectsAITEX_best_pipeline_initial_params = [
    27,  # MaskWidthEMM
    31,  # MaskHeightEMM
    11,  # Gap
    1,  # Mode
    21,  # MaskWidthVT
    9,  # MaskHeightVT
    0.2000001,  # StdDevScale
    76,  # AbsThreshold
    'not_equal'  # LightDark
]

FabricDefectsAITEX_best_pipeline_bounds = [
    [v for v in range(3, 101, 2)],  # MaskWidthEMM
    [v for v in range(3, 101, 2)],  # MaskHeightEMM
    [v for v in range(1, 50)],  # Gap
    [0, 1],  # Mode
    [v for v in range(3, 101, 2)],  # MaskWidthVT
    [v for v in range(3, 101, 2)],  # MaskHeightVT
    [round(v * 0.1, 1) for v in range(1, 50)],  # StdDevScale
    [v for v in range(0, 255, 1)],  # AbsThreshold
    ['dark', 'light', 'not_equal']  # LightDark
]

FabricDefectsAITEX_training_source_path = os.path.join(EVIAS_SRC_PATH, "FabricDefectsAITEX",
                                                       "train")
