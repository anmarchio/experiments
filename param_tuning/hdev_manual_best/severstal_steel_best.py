"""
=======================================
severstal-steel_best_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, get_var_threshold_code
from settings import EVIAS_SRC_PATH


def get_severstal_steel_best_pipeline(params, dataset_path=None):
    pipeline_name = "severstal-steel_best_pipeline"

    if dataset_path is None:
        dataset_path = "/severstal-steel/train_cgp/images"

        # Parameters
        param_lines = (
                "<l>        Filter := '" + str(params[0]) + "'</l>\n"
                                                            "<l>        Alpha := " + str(params[1]) + "</l>\n"
                                                                                                      "<l>        Low := " + str(
            params[2]) + "</l>\n"
                         "<l>        High := " + str(params[3]) + "</l>\n"
                                                                  "<l>        NonMaximumSuppression := '" + str(
            params[4]) + "'</l>\n"
                         "<c></c>\n"
                         "<l>        Min := " + str(params[5]) + "</l>\n"
                                                                 "<l>        Max := " + str(params[6]) + "</l>\n"
                                                                                                         "<c></c>\n"
                                                                                                         "<l>        Iterations := " + str(
            params[7]) + "</l>\n"
                         "<l>        A := " + str(params[8]) + "</l>\n"
                                                               "<l>        B := " + str(params[9]) + "</l>\n"
                                                                                                     "<c></c>\n"
        )

        # Core pipeline
        core_code = (
            "<c>* EdgesImage</c>\n"
            "<l>        edges_image(Image, ImageEdges, ImaDir, Filter, Alpha, NonMaximumSuppression, Low, High)</l>\n"
            "<c></c>\n"
            "<c>* Threshold</c>\n"
            "<l>        threshold(ImageEdges, RegionThresh, Min, Max)</l>\n"
            "<c></c>\n"
            "<c>* Dilation1 (Ellipse SE)</c>\n"
            "<l>        tuple_max2(A, B, max_rad)</l>\n"
            "<l>        phi := 0.0</l>\n"
            "<l>        longer := A</l>\n"
            "<l>        shorter := B</l>\n"
            "<l>        if (shorter > longer)</l>\n"
            "<l>            tmp := shorter</l>\n"
            "<l>            shorter := longer</l>\n"
            "<l>            longer := tmp</l>\n"
            "<l>        endif</l>\n"
            "<l>        tuple_ceil(max_rad + 1, max_rad_ceil)</l>\n"
            "<l>        gen_ellipse(StructElement, max_rad_ceil, max_rad_ceil, phi, longer, shorter)</l>\n"
            "<l>        dilation1(RegionThresh, StructElement, Region, Iterations)</l>\n"
        )

        return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


severstal_steel_best_pipeline_initial_params = [
    'canny',  # Filter
    1.2,  # Alpha
    5,  # Low
    20,  # High
    'nms',  # NonMaximumSuppression
    65,  # Min
    240,  # Max
    1,  # Iterations
    18,  # A
    18  # B
]

severstal_steel_bounds = [
    ['canny', 'lanser1', 'lanser2', 'shen', 'sobel_fast'],  # Filter
    [round(0.1 * v, 1) for v in range(1, 50)],  # Alpha
    [v for v in range(1, 255)],  # Low
    [v for v in range(1, 255)],  # High
    ['nms', 'inms', 'hvnms', 'none'],  # NonMaximumSuppression
    [v for v in range(1, 255)],  # Min
    [v for v in range(1, 255)],  # Max
    [v for v in range(1, 10)],  # Iterations
    [v for v in range(1, 50)],  # A
    [v for v in range(1, 50)]  # B
]

severstal_steel_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                    "severstal-steel", "train_cgp")
