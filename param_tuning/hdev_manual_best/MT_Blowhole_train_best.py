"""
=======================================
MT_Blowhole_train_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MT_Blowhole_train_best_pipeline(params, dataset_path=None):
    pipeline_name = "MT_Blowhole_train_best_pipeline"

    if dataset_path is None:
        dataset_path = "/Magnetic-Tile-Defect/MT_Blowhole_train/images"

    # Parameters
    param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        Radius := " + str(params[1]) + "</l>\n" + \
                      "<l>        Margin := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<l>        median_image(Image, ImageMedian, MaskType, Radius, Margin)</l>\n"
            "<l>        local_threshold(ImageMedian, Region, Method, LightDark, ['mask_size','scale'], [MaskSize, Scale])</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MT_Blowhole_train_best_pipeline_initial_params = [
    'circle',  # MaskType
    2,  # Radius
    255,  # Margin
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    15,  # MaskSize
    0.3  # Scale
]

MT_Blowhole_train_best_pipeline_bounds = [
    ['circle', 'square', 'mask'],  # MaskType
    [v for v in range(1, 20)],  # Radius
    [0, 128, 255],  # Margin (numeric values)
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 101, 2)],  # MaskSize
    [round(0.1 * v, 1) for v in range(1, 50)]  # Scale
]

MT_Blowhole_train_training_source_path = os.path.join(EVIAS_SRC_PATH, "Magnetic-Tile-Defect", "MT_Blowhole_train")
