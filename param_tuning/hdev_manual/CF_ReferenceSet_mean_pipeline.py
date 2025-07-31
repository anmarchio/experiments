
"""
=========================
CF_ReferenceSet_mean_pipeline.py
=========================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH

def get_CF_ReferenceSet_mean_pipeline(params, dataset_path=None):
    pipeline_name = "CF_ReferenceSet_mean_pipeline"

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
    core_code = "<l>        var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, LightDark)</l>\n" \
                "<l>        connection(Region, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


CF_ReferenceSet_mean_pipeline_initial_params = [
    23,
    15,
    0.7000001,
    85,
    'not_equal'
]

CF_ReferenceSet_mean_pipeline_bounds = [
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v / 10.0) for v in range(0, 10, 1)],
    [v for v in range(0, 128, 1)],
    ['dark', 'light']
]

CF_ReferenceSet_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2", "CF_ReferenceSet")
