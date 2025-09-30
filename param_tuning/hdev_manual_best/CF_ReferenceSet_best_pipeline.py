
"""
=========================
CF_ReferenceSet_best_pipeline.py
=========================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH

def get_CF_ReferenceSet_best_pipeline(params, dataset_path = None):
    pipeline_name = "CF_ReferenceSet_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Aircarbon2/CF_ReferenceSet/images"

    # Parameters
    param_lines = "<l>        MaskWidth := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[1]) + "</l>\n" + \
                      "<l>        StdDevScale := " + str(params[2]) + "</l>\n" + \
                      "<l>        AbsThreshold := " + str(params[3]) + "</l>\n" + \
                      "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                      "<c></c>\n"

    # Core Pipeline Code
    core_code = ("<l>        var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, LightDark)</l>\n" \
                    "<l>        connection(Region, Region)</l>\n"
                 )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CF_ReferenceSet_best_pipeline_initial_params = [
    23,  # MaskWidth
    15,  # MaskHeight
    0.7000001,  # StdDevScale
    85,  # AbsThreshold
    'not_equal'  # LightDark
]

CF_ReferenceSet_best_pipeline_bounds = [
    [v for v in range(3, 101, 2)],  # MaskWidth
    [v for v in range(3, 101, 2)],  # MaskHeight
    [round(v * 0.1, 1) for v in range(1, 50)],  # StdDevScale
    [v for v in range(0, 255, 1)],  # AbsThreshold
    ['dark', 'light', 'not_equal']  # LightDark
]

CF_ReferenceSet_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2", "CF_ReferenceSet")
