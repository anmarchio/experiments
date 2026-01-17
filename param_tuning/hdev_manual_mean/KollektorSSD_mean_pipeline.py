"""
============================
KollektorSSD_mean_pipeline.py
============================
"""
import os

from param_tuning.hdev_manual_mean.hdev_manual_utils import get_custom_hdev_pipeline_code, scale_to_gray
from settings import EVIAS_SRC_PATH


def get_KollektorSSD_mean_pipeline(params, dataset_path = None):
    pipeline_name = "KollektorSSD_mean_pipeline"

    if dataset_path is None:
        dataset_path = "/KolektorSDD/kos10/images"

    # Parameters
    param_lines = ""

    core_code = "<l>        equ_histo_image(Image, Image)</l>\n" + \
                "<l>        convert_image_type(Image, Image, 'int2')</l>\n" +\
                "<c>        </c>\n" + \
                scale_to_gray() + \
                "<l>        zero_crossing(ScaledImage, Region)</l>\n"

    return get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code)


KollektorSSD_mean_pipeline_initial_params = []

KollektorSSD_mean_pipeline_bounds = []

KollektorSSD_training_source_path = os.path.join(EVIAS_SRC_PATH, "KolektorSDD",
                                                       "kos10")
