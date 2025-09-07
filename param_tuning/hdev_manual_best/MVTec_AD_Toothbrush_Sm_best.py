"""
=======================================
MVTec_AD_Toothbrush_Sm_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Toothbrush_Sm_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Toothbrush_Sm_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/toothbrush_small_train/images"

        # Parameters
        param_lines = (
                "<l>        FilterType := '" + str(params[0]) + "'</l>\n"
                                                                "<l>        MaskSize := " + str(params[1]) + "</l>\n"
                                                                                                             "<c></c>\n"
                                                                                                             "<l>        MaskWidth := " + str(
            params[2]) + "</l>\n"
                         "<l>        MaskHeight := " + str(params[3]) + "</l>\n"
                                                                        "<l>        StdDevScale := " + str(
            params[4]) + "</l>\n"
                         "<l>        AbsThreshold := " + str(params[5]) + "</l>\n"
                                                                          "<l>        LightDark := '" + str(
            params[6]) + "'</l>\n"
                         "<c></c>\n"
        )

        # Core pipeline
        core_code = (
            "<c>* SobelAmp</c>\n"
            "<l>        sobel_amp(Image, Image, FilterType, MaskSize)</l>\n"
            "<c></c>\n"
            "<c>* VarThreshold with type handling</c>\n"
            "<l>        get_image_type(Image, Type)</l>\n"
            "<l>        if(Type != 'byte' and Type != 'int2' and Type != 'int4' and Type != 'uint2' and Type != 'real')</l>\n"
            "<l>            min_max_gray(Image, Image, 0, Min, Max, Range)</l>\n"
            "<l>            if (not((255 >= Max) and (Min >= 0)))</l>\n"
            "<l>                if ((Max - Min) > 0)</l>\n"
            "<l>                    Mult := 255.0 / (Max - Min)</l>\n"
            "<l>                else</l>\n"
            "<l>                    Mult := 255.0</l>\n"
            "<l>                endif</l>\n"
            "<l>                Add := -Mult * Min</l>\n"
            "<l>                scale_image(Image, Image, Mult, Add)</l>\n"
            "<l>            else</l>\n"
            "<l>                scale_image(Image, Image, 1, 0)</l>\n"
            "<l>            endif</l>\n"
            "<l>            StandardType := 'byte'</l>\n"
            "<l>            convert_image_type(Image, Image, 'byte')</l>\n"
            "<l>            var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, LightDark)</l>\n"
            "<l>        else</l>\n"
            "<l>            var_threshold(Image, Region, MaskWidth, MaskHeight, StdDevScale, AbsThreshold, LightDark)</l>\n"
            "<l>        endif</l>\n"
            "<c></c>\n"
            "<c>* AreaToRectangle</c>\n"
            "<l>        area_center(Region, Area, Row, Column)</l>\n"
            "<l>        Num := |Area|</l>\n"
            "<l>        gen_empty_region(Rectangles)</l>\n"
            "<l>        for Index1 := 1 to Num by 1</l>\n"
            "<l>            select_obj(Region, obj, Index1)</l>\n"
            "<l>            smallest_rectangle1(obj, Row11, Column11, Row21, Column21)</l>\n"
            "<l>            gen_rectangle1(Rectangle, Row11, Column11, Row21, Column21)</l>\n"
            "<l>            union2(Rectangles, Rectangle, Rectangles)</l>\n"
            "<l>        endfor</l>\n"
            "<l>        Region := Rectangles</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Toothbrush_Sm_best_pipeline_initial_params = [
    'y',  # FilterType
    7,  # MaskSize
    5,  # MaskWidth
    17,  # MaskHeight
    0.9000002,  # StdDevScale
    76,  # AbsThreshold
    'dark'  # LightDark
]

MVTec_AD_Toothbrush_Sm_best_pipeline_bounds = [
    ['x', 'y', 'sum_abs', 'sum_sqrt', 'x_binomial', 'y_binomial'],  # FilterType
    [3, 5, 7, 9, 11],  # MaskSize
    [v for v in range(1, 50)],  # MaskWidth
    [v for v in range(1, 50)],  # MaskHeight
    [round(0.1 * v, 1) for v in range(1, 30)],  # StdDevScale
    [v for v in range(0, 255)],  # AbsThreshold
    ['dark', 'light', 'not_equal']  # LightDark
]

MVTec_AD_Toothbrush_Sm_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                        "MVTecAnomalyDetection", "toothbrush_small_train")
