"""
=======================================
MVTec_AD_Leather_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_area_to_rectangle
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Leather_mean_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Leather_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/leather_train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * Path 1</c>\n" \
                "<c>        * SobalAmp</c>\n" \
                "<l>        get_image_type(Image, Type)</l>\n" + \
                "<l>        if(FilterType == 'x_binomial' or FilterType == 'y_binomial')</l>\n" + \
                "<l>            if(Type != 'byte' and Type != 'int2' and Type != 'real')</l>\n" + \
                "<l>                convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>            endif</l>\n" + \
                "<l>        elseif(Type != 'byte' and Type != 'int2' and Type != 'uint2' and Type != 'real')</l>\n" + \
                "<l>            convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>        endif</l>\n" + \
                "<l>        sobel_amp(Image, Image1, FilterType, MaskSize)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Path 2</c>\n" \
                "<c>        * SigmaImage</c>\n" \
                "<l>        sigma_image(Image, Image2, MaskHeight, MaskWidth, Sigma)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Local Threshold</c>\n" \
                "<l>        local_threshold(Image2, Region2, Method, LightDark, ['mask_size', 'scale'], [MaskSize, Scale])</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Merge</c>\n" \
                "<c>        * CloseEdges</c>\n" \
                "<l>        convert_image_type(Image1, Image1, 'byte')</l>\n" + \
                "<l>        close_edges(Region2, Image1, Region, MinAmplitude)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Closing</c>\n" + \
                "<l>        gen_rectangle1(RectangleStructElement, 0, 0, A, B)</l>\n" + \
                "<l>        closing(Region, RectangleStructElement, Region) </l>\n" + \
                "<c></c>\n"

    raise ValueError("!!!NOT matching with ground truth MCC, FIX !!!")

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Leather_mean_pipeline_initial_params = [
    4,
    28,
    30,
    'adapted_std_deviation',
    'light',
    21,
    0.5
]

MVTec_AD_Leather_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5]
]

MVTec_AD_Leather_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "MVTecAnomalyDetection", "leather_train")
