"""
=======================================
MVTec_AD_Pultrusion_Resin_Augmtd_mean_pipeline
=======================================
"""
import os

from param_tuning.hdev_manual.hdev_manual_utils import get_custom_hdev_pipeline_code
from settings import EVIAS_SRC_PATH


def get_Pultrusion_Resin_Augmtd_mean_pipeline(params):
    pipeline_name = "Pultrusion_Resin_Augmtd_mean_pipeline"
    dataset_path = "/Pultrusion/resin_cgp_augmntd/train/images"

    # Parameters
    param_lines = "<l>        A := " + str(params[0]) + "</l>\n" + \
                  "<l>        B := " + str(params[1]) + "</l>\n" + \
                  "<l>        GrayValueMax := " + str(params[2]) + "</l>\n" + \
                  "<l>        Method := '" + str(params[3]) + "'</l>\n" + \
                  "<l>        LightDark := '" + str(params[4]) + "'</l>\n" + \
                  "<c></c>\n"

    # Core Pipeline Code
    core_code = "<c>        * GrayErosion</c>\n" + \
                "<c>        * with struct element circle</c>\n" + \
                "<c>        * StructElementType Ellipse</c>\n" + \
                "<c>        * using A, B and C as shape_params</c>\n" + \
                "<c>        </c>\n" + \
                "<l>        get_image_type(Image, Type)</l>\n" + \
                "<l>        gen_disc_se(StructElement, Type, A, B, GrayValueMax)</l>\n" + \
                "<l>        gray_erosion(Image, StructElement, Image)</l>\n" + \
                "<c>        </c>\n" + \
                "<c>        * BinaryThreshold</c>\n" + \
                "<l>        binary_threshold(Image, Region, Method, LightDark, UsedThreshold)</l>\n" \
                "<c>        </c>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


Pultrusion_Resin_Augmtd_mean_pipeline_initial_params = [
    30,
    30,
    0,
    'max_separability',
    'light'
]

Pultrusion_Resin_Augmtd_mean_pipeline_bounds = [
    [v for v in range(1, 30, 1)],
    [v for v in range(1, 30, 1)],
    [0, 1, 2, 5, 10, 20, 30, 40],
    ['max_separability', 'smooth_histo'],
    ['dark', 'light'],
]

Pultrusion_Resin_Augmtd_training_source_path = os.path.join(EVIAS_SRC_PATH,
                                                            "Pultrusion", "resin_cgp_augmntd", "train")
