"""
AirCarbon2_t_8_jpg_mean.py
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def AirCarbon2_t_8_jpg_mean_pipeline(params):
    pipeline_name = "AirCarbon2_t_8.jpg_mean_pipeline"
    dataset_path = "/Aircarbon2/Blende5_6_1800mA_rov/training/t_8.jpg/images"

    # Parameters
    # 'lines', 'y', 5, 'adapted_std_deviation', 'dark', 15, 0.3
    param_lines = "<l>        DiffusionCoefficient := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Contrast := " + str(params[1]) + "</l>\n" + \
                  "<l>        Theta := " + str(params[2]) + "</l>\n" + \
                  "<l>        Iterations := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        MaskWidth := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskHeight := " + str(params[5]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[6]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[7]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[8]) + "'</l>\n\n"

    # Core Pipeline Code
    core_code = "<l>        anisotropic_diffusion(Image, Image, DiffusionCoefficient, Contrast, Theta, " \
                "Iterations)</l>\n" \
                "<c></c>\n" \
                "<l>        var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, " \
                "LightDark)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


AirCarbon2_t_8_jpg_mean_pipeline_initial_params = [
    'parabolic',
    100,
    3.0,
    3,
    29,
    9,
    0.9000002,
    11,
    'light'
]

AirCarbon2_t_8_jpg_mean_pipeline_bounds = [
    ['weickert', 'perona-malik', 'parabolic'],
    [3, 5, 10, 20, 50, 100],
    [0.5, 1.0, 3.0],
    [1, 3, 10, 100, 500],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v / 10.0) for v in range(0, 10, 1)],
    [v for v in range(0, 128, 1)],
    ['dark', 'equal', 'light', 'not_equal']
]

AirCarbon2_t_8_jpg_training_source_path = os.path.join(EVIAS_SRC_PATH, "Aircarbon2", "Blende5_6_1800mA_rov",
                                                       "training", "t_8.jpg")