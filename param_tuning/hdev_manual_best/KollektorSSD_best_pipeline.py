"""
============================
KollektorSSD_best_pipeline.py
============================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_KollektorSSD_best_pipeline(params, dataset_path=None):
    pipeline_name = "KollektorSSD_best_pipeline"

    if dataset_path is None:
        dataset_path = "/KolektorSDD/kos10/images"

    # Parameters
    param_lines = "<l>        Sigma := " + str(params[0]) + "</l>\n" + \
                      "<l>        Rho := " + str(params[1]) + "</l>\n" + \
                      "<l>        Theta := " + str(params[2]) + "</l>\n" + \
                      "<l>        Iterations := " + str(params[3]) + "</l>\n" + \
                      "<l>        Method := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[6]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[7]) + "</l>\n" + \
                      "<c></c>\n"

    # Core Pipeline Code
    core_code = "<l>        coherence_enhancing_diff(Image, DiffImage, Sigma, Rho, Theta, Iterations)</l>\n" \
                    "<c></c>\n" \
                    "<l>        access_channel(DiffImage, ImageAmp, 1)</l>\n" \
                    "<l>        convert_image_type(DiffImage, DiffImage, 'byte')</l>\n" \
                    "<l>        local_threshold(DiffImage, Region, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


KollektorSSD_best_pipeline_initial_params = [
    0.4,  # Sigma
    2,  # Rho
    0.3,  # Theta
    23,  # Iterations 230
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSize
    0.3  # Scale
]

KollektorSSD_best_pipeline_bounds = [
    [round(v * 0.1, 1) for v in range(1, 50)],  # Sigma
    [v for v in range(1, 10)],  # Rho
    [round(v * 0.1, 1) for v in range(1, 50)],  # Theta
    [v for v in range(1, 1000)],  # Iterations
    ['adapted_std_deviation', 'mean', 'max'],  # Method (common LocalThreshold methods)
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 101, 2)],  # MaskSize
    [round(v * 0.1, 1) for v in range(1, 50)]  # Scale
]

KollektorSSD_training_source_path = os.path.join(EVIAS_SRC_PATH, "KolektorSDD",
                                                 "kos10")
