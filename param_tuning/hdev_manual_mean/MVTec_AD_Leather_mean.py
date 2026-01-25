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
    param_lines = "<l>        FilterType := '" + str(params[0]) + "'</l>\n" + \
                  "<l>        MaskSize := " + str(params[1]) + "</l>\n" + \
                  "<l>        MaskHeight := " + str(params[2]) + "</l>\n" + \
                  "<l>        MaskWidth := " + str(params[3]) + "</l>\n" + \
                  "<l>        Sigma := " + str(params[4]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[5]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[6]) + "'</l>\n" + \
                  "<l>        MaskSize2 := " + str(params[7]) + "</l>\n" + \
                  "<l>        Scale := " + str(params[8]) + "</l>\n" + \
                  "<l>        MinAmplitude := " + str(params[9]) + "</l>\n" + \
                  "<l>        A := " + str(params[10]) + "</l>\n" + \
                  "<l>        B := " + str(params[11]) + "</l>\n" + \
                  "<l>        C := 0.0</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * Path 1</c>\n" \
                "<c>        * SobalAmp</c>\n" \
                "<l>        get_image_type(Image, ImageType)</l>\n" + \
                "<l>        if(ImageType == 'x_binomial' or ImageType == 'y_binomial')</l>\n" + \
                "<l>            if(ImageType != 'byte' and ImageType != 'int2' and ImageType != 'real')</l>\n" + \
                "<l>                convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>            endif</l>\n" + \
                "<l>        elseif(ImageType != 'byte' and ImageType != 'int2' and ImageType != 'uint2' and ImageType != 'real')</l>\n" + \
                "<l>            convert_image_type(Image, Image, 'byte')</l>\n" + \
                "<l>        endif</l>\n" + \
                "<l>        sobel_amp(Image, Image1, FilterType, MaskSize)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Path 2</c>\n" \
                "<c>        * SigmaImage</c>\n" \
                "<l>        sigma_image(Image, Image2, MaskHeight, MaskWidth, Sigma)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * Local Threshold</c>\n" \
                "<l>        local_threshold(Image2, Region2, Method, LightDark, ['mask_size', 'scale'], [MaskSize2, Scale])</l>\n" + \
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

    #raise ValueError("!!!NOT matching with ground truth MCC, FIX !!!")

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Leather_mean_pipeline_initial_params = [
    'y_binomial', # filter type
    3, # mask size
    17, # mask height
    3, # mask width
    134, # sigma
    'adapted_std_deviation', # method
    'light', # lightdark
    31, # mask size 2
    0.2, # scale
    79, # min amplitude
    5, # A
    30 # B
]

MVTec_AD_Leather_mean_pipeline_bounds = [
    ['x_binomial', 'y_binomial', 'sum_abs', 'x', 'y', 'binomial'],
    [1, 3, 5, 7, 9],
    [3, 7, 11, 15, 17, 21, 25, 29],
    [1, 3, 5, 7, 9, 11, 13, 15],
    [v for v in range(1, 255, 1)],
    ['adapted_std_deviation'],
    ['dark', 'light'],
    [15, 21, 31],
    [0.2, 0.3, 0.5],
    [v for v in range(1, 255, 1)],
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)]
]

MVTec_AD_Leather_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "MVTecAnomalyDetection", "leather_train")
