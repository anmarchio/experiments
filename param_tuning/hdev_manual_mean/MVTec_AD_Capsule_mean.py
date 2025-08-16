"""
=======================================
MVTec_AD_Capsule_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Capsule_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Capsule_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/capsule_crack_train/images"

    # Parameters
    param_lines = "<l>        Filter := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        Alpha := " + str(params[1]) + "</l>\n" + \
                  "<l>        Low := " + str(params[2]) + "</l>\n" + \
                  "<l>        High := " + str(params[3]) + "</l>\n" + \
                  "<l>        NonMaximumSuppression := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        FilterType := '" + str(params[5]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[3]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[3]) + "</l>\n" + \
                  "<l>        StdDevScale := " + str(params[3]) + "</l>\n" + \
                  "<l>        AbsThreshold := " + str(params[3]) + "</l>\n" + \
                  "<l>        LightDark := '" + str(params[5]) + "'</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * EdgesImage</c>\n" \
                "<l>        edges_image(Image, Image, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n" + \
                "<c></c>\n" + \
                "<c>        * SobelAmp</c>\n" + \
                "<l>        get_image_type(Image, Type)  </l>\n" + \
                "<l>        if(Type != 'byte' and Type != 'uint2' and Type != 'real')</l>\n" + \
                "<l>            convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>        endif</l>\n" + \
                "<l>        sobel_amp(Image, Image, FilterType, MaskSize)</l>\n" + \
                "<c></c>\n" + \
                get_var_threshold_code()

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Capsule_mean_pipeline_initial_params = [
    'canny',
    1.1,
    5,
    25,
    'nms',
    'y',
    7,
    23,
    25,
    -0.09999993,
    19,
    'not_equal'

]

MVTec_AD_Capsule_mean_pipeline_bounds = [
    ['canny'],
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
    [5, 10, 15, 20, 25, 30, 40],
    [5, 10, 15, 20],
    ['nms', 'inms', 'hvnms', 'none'],
    ['y', 'y_binomial', 'x', 'x_binomial'],
    [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    [v for v in range(3, 30, 2)],
    [v for v in range(3, 30, 2)],
    [float(v) / 10.0 for v in range(-10, 10, 1)],
    [0, 128],
    ['not_equal', 'light', 'equal', 'dark']
]

MVTec_AD_Capsule_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                     "MVTecAnomalyDetection", "capsule_crack_train")
