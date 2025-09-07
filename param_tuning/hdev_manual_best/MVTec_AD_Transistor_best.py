"""
=======================================
Transistor_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_crop_rectangle_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Transistor_best_pipeline(params, dataset_path = None):
    pipeline_name = "MVTec_AD_Transistor_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/transistor_damaged_case_train/images"

        # Parameters
        param_lines = (
                "<l>        MaskWidth := " + str(params[0]) + "</l>\n"
                                                              "<l>        MaskHeight := " + str(params[1]) + "</l>\n"
                                                                                                             "<l>        Gap := " + str(
            params[2]) + "</l>\n"
                         "<l>        Mode := " + str(params[3]) + "</l>\n"
                                                                  "<c></c>\n"
                                                                  "<l>        FilterType := '" + str(
            params[4]) + "'</l>\n"
                         "<l>        MaskSize := " + str(params[5]) + "</l>\n"
                                                                      "<c></c>\n"
                                                                      "<l>        Method := '" + str(
            params[6]) + "'</l>\n"
                         "<l>        LightDark := '" + str(params[7]) + "'</l>\n"
                                                                        "<l>        MaskSizeThresh := " + str(
            params[8]) + "</l>\n"
                         "<l>        Scale := " + str(params[9]) + "</l>\n"
                                                                   "<c></c>\n"
        )

        # Core pipeline
        core_code = (
            "<c>* EliminateMinMax</c>\n"
            "<l>        eliminate_min_max(Image, ImageElim, MaskWidth, MaskHeight, Gap, Mode)</l>\n"
            "<c></c>\n"
            "<c>* SobelAmp</c>\n"
            "<l>        sobel_amp(ImageElim, ImageAmp, FilterType, MaskSize)</l>\n"
            "<c></c>\n"
            "<c>* LocalThreshold</c>\n"
            "<l>        access_channel(ImageAmp, ImageAmp, 1)</l>\n"
            "<l>        convert_image_type(ImageAmp, ImageAmp, 'byte')</l>\n"
            "<l>        local_threshold(ImageAmp, Region, Method, LightDark, ['mask_size','scale'], [MaskSizeThresh, Scale])</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Transistor_best_pipeline_initial_params = [
    13,  # MaskWidth
    17,  # MaskHeight
    21,  # Gap
    1,  # Mode
    'y_binomial',  # FilterType
    5,  # MaskSize
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    31,  # MaskSizeThresh
    0.2  # Scale
]

MVTec_AD_Transistor_best_pipeline_bounds = [
    [v for v in range(1, 50)],  # MaskWidth
    [v for v in range(1, 50)],  # MaskHeight
    [v for v in range(1, 100)],  # Gap
    [0, 1],  # Mode
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 100, 2)],  # MaskSizeThresh
    [round(0.1 * v, 1) for v in range(1, 20)]  # Scale
]

MVTec_AD_Transistor_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "transistor_damaged_case_train")
