"""
=======================================
MVTec_AD_Cable_Missing_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_MVTec_AD_Cable_Missing_best_pipeline(params, dataset_path=None):
    pipeline_name = "MVTec_AD_Cable_Missing_best_pipeline"

    if dataset_path is None:
        # Default dataset path for MVTec AD Cable Missing
        dataset_path = "/MVTecAnomalyDetection/cable_missing_train/images"

    # Parameters
    param_lines = "<l>        MaskType := '" + str(params[0]) + "'</l>\n" + \
                      "<l>        Radius := " + str(params[1]) + "</l>\n" + \
                      "<l>        Margin := " + str(params[2]) + "</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                      "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        Min := " + str(params[5]) + "</l>\n" + \
                      "<l>        Max := " + str(params[6]) + "</l>\n" + \
                      "<l>        Features := '" + str(params[7]) + "'</l>\n" + \
                      "<c></c>\n" + \
                      "<l>        A := " + str(params[8]) + "</l>\n" + \
                      "<l>        B := " + str(params[9]) + "</l>\n" + \
                      "<l>        C := 0.392699</l>\n" + \
                      "<c></c>\n"

    # Core pipeline
    core_code = (
            "<l>        median_image(Image, ImageMedian, MaskType, Radius, Margin)</l>\n"
            "<c></c>\n"
            "<l>        binary_threshold(ImageMedian, RegionBinary, Method, LightDark, UsedThreshold)</l>\n"
            "<c></c>\n"
            "<l>        select_shape(RegionBinary, RegionSelected, Features, 'and', Min, Max)</l>\n"
            "<c></c>\n"
            "<l>        gen_rectangle2(RectangleStructElement, 0, 0, C, A, B)</l>\n"
            "<l>        closing(RegionSelected, RectangleStructElement, RegionClosed)</l>\n"
            "<c></c>\n"
            "<l>        connection(RegionClosed, Region)</l>\n"
        )

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


MVTec_AD_Cable_Missing_best_pipeline_initial_params = [
    'circle',  # MaskType
    54,  # Radius
    90,  # Margin
    'smooth_histo',  # Method
    'dark',  # LightDark
    45,  # Min
    99999,  # Max
    'dist_mean',  # Features
    4,  # A
    15  # B
]

MVTec_AD_Cable_Missing_best_pipeline_bounds = [
    ['circle', 'square', 'mask'],                 # MaskType
    [v for v in range(1, 200)],                   # Radius
    ['\'mirrored\'', '\'cyclic\'', '\'continued\'', 0, 30, 60, 90, 120, 150, 180, 210, 240, 255],   # Margin
    ['smooth_histo', 'max_separability', 'entropy', 'otsu'],  # Method
    ['dark', 'light'],                            # LightDark
    [v for v in range(0, 500)],                   # Min
    [v for v in range(1, 100000)],                # Max
    ['area', 'width', 'height', 'dist_mean'],     # Features
    [v for v in range(1, 50)],                    # A
    [v for v in range(1, 50)]                    # B
]

MVTec_AD_Cable_Missing_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                           "MVTecAnomalyDetection", "cable_missing_train")
