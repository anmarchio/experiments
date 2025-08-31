"""
=======================================
MVTec_AD_Bottle_Broken_Lg_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Bottle_Broken_Lg_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Bottle_Broken_Lg_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/bottle_broken_large_train/images"

        # Parameters
        param_lines = "<l>        MaskWidth := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskHeight := " + str(params[1]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[2]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[3]) + "'</l>\n" + \
                      "<c></c>\n"

        # Core pipeline
        core_code = (
            "<l>        mean_image(Image, ImageMean, MaskWidth, MaskHeight)</l>\n"
            "<l>        binary_threshold(ImageMean, Region, Method, LightDark)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Bottle_Broken_Lg_best_pipeline_initial_params = [
    347,  # MaskWidth
    283,  # MaskHeight
    'max_separability',  # Method
    'dark'  # LightDark
]

MVTec_AD_Bottle_Broken_Lg_best_pipeline_bounds = [
    [v for v in range(3, 501, 2)],  # MaskWidth
    [v for v in range(3, 501, 2)],  # MaskHeight
    ['max_separability', 'smooth_histo'],  # Method
    ['dark', 'light']  # LightDark
]

MVTec_AD_Bottle_Broken_Lg_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                              "MVTecAnomalyDetection", "bottle_broken_large_train")
