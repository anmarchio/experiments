"""
=======================================
MVTec_AD_Leather_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_area_to_rectangle
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Leather_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Leather_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/leather_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                      "<l>        B := " + str(params[1]) + "</l>\n" + \
                      "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<c>* GrayErosion</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n"
            "<l>        gen_disc_se(SE, Type, A, B, GrayValueMax)</l>\n"
            "<l>        gray_erosion(Image, SE, ImageEroded)</l>\n"
            "<c></c>\n"
            "<c>* LocalThreshold</c>\n"
            "<l>        local_threshold(ImageEroded, RegionThresh, Method, LightDark, ['mask_size','scale'], [MaskSize, Scale])</l>\n"
            "<c></c>\n"
            + get_area_to_rectangle +
            "<l>        Region := Rectangles</l>\n"
    )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Leather_best_pipeline_initial_params = [
    19,  # A
    8,  # B
    1,  # GrayValueMax
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    15,  # MaskSize
    0.3  # Scale
]

MVTec_AD_Leather_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)],  # B
    [v for v in range(0, 255)],  # GrayValueMax
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 100, 2)],  # MaskSize
    [round(0.1 * v, 1) for v in range(1, 20)]  # Scale
]

MVTec_AD_Leather_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                     "MVTecAnomalyDetection", "leather_train")
