"""
=======================================
MVTec_AD_Cable_Missing_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Cable_Missing_mean_pipeline(params):
    pipeline_name = "MVTec_AD_Cable_Missing_mean_pipeline"
    dataset_path = "/MVTecAnomalyDetection/cable_missing_train/images"

    # Parameters
    param_lines = "<l>        DiffusionCoefficient := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Contrast := " + str(params[1]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[2]) + "</l>\n" + \
                  "<l>        Iterations := " + str(params[3]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * AnisotropicDiffusion</c>\n" \
                "<l>        anisotropic_diffusion(Image, Image, DiffusionCoefficient, Contrast, Theta, " \
                "Iterations)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * BinaryThreshold</c>\n" + \
                "<l>        binary_threshold(Image, Region, Method, LightDark, UsedThreshold)</l>\n" + \
                "<c></c>\n" + \
                "<l>        * Connection</l>\n" + \
                "<l>        connection(Region, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Cable_Missing_mean_pipeline_initial_params = [
    'perona-malik',
    10,
    3,
    60,
    'smooth_histo',
    'dark'
]

MVTec_AD_Cable_Missing_mean_pipeline_bounds = [
    ['perona-malik', 'weickert', 'parabolic'],
    [2, 5, 10, 20, 50, 100],
    [0.5, 1.0, 3.0],
    [v for v in range(1, 60, 1)],  # [1, 3, 10, 100, 500]
    ['max_separability', 'smooth_histo'],
    ['light', 'dark']
]

MVTec_AD_Cable_Missing_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "cable_missing_train")
