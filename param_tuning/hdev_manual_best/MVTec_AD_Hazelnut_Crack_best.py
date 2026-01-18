"""
=======================================
MVTec_AD_Hazelnut_Crack_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_area_to_rectangle
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Hazelnut_Crack_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Hazelnut_Crack_best_pipeline"

    if dataset_path is None:
        dataset_path = "/MVTecAnomalyDetection/hazelnut_crack_train/images"

    # Parameters
    param_lines = "<l>        MaskHeightSigma := " + str(params[0]) + "</l>\n" + \
                      "<l>        MaskWidthSigma := " + str(params[1]) + "</l>\n" + \
                      "<l>        Sigma := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                      "<l>        MaskSize := " + str(params[5]) + "</l>\n" + \
                      "<l>        Scale := " + str(params[6]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[7]) + "</l>\n" + \
                      "<l>        B := " + str(params[8]) + "</l>\n" + \
                      "<l>        C := 0.785398</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<l>        sigma_image(Image, ImageSigma, MaskWidthSigma, MaskHeightSigma, Sigma)</l>\n"
            "<c>        </c>\n"
            "<l>        local_threshold(ImageSigma, RegionThresh, Method, LightDark, ['mask_size','scale'], [MaskSize, Scale])</l>\n"
            "<c>        </c>\n"
            "<c>        * AreaToRectangle\n"
            + get_area_to_rectangle() +
            "<l>        RegionRect := Rectangles</l>\n"
            "<c>        </c>\n"
            "<c>        * Closing (Ellipse SE)\n"
            "<l>        tuple_max2(A, B, max_rad)\n"
            "<l>        phi := C\n"
            "<l>        longer := A\n"
            "<l>        shorter := B\n"
            "<l>        if (shorter > longer)\n"
            "<l>                tmp := shorter\n"
            "<l>                shorter := longer\n"
            "<l>                longer := tmp\n"
            "<l>        endif\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)\n"
            "<l>        gen_ellipse(StructElement2, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<l>        closing(RegionRect, StructElement2, Region)</l>\n"
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


# Initial Parameters
MVTec_AD_Hazelnut_Crack_best_pipeline_initial_params = [
    9,  # MaskHeightSigma
    7,  # MaskWidthSigma
    54,  # Sigma
    'adapted_std_deviation',  # Method
    'dark',  # LightDark
    15,  # MaskSize
    0.5,  # Scale
    17,  # A
    12  # B
]

MVTec_AD_Hazelnut_Crack_best_pipeline_bounds = [
    [v for v in range(3, 50, 2)],  # MaskHeightSigma
    [v for v in range(3, 50, 2)],  # MaskWidthSigma
    [v for v in range(1, 100)],  # Sigma
    ['adapted_std_deviation', 'mean', 'max'],  # Method
    ['dark', 'light'],  # LightDark
    [v for v in range(3, 100, 2)],  # MaskSize
    [round(0.1 * v, 1) for v in range(1, 20)],  # Scale
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)]  # B
]

MVTec_AD_Hazelnut_Crack_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "MVTecAnomalyDetection", "hazelnut_crack_train")
