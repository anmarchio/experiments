from param_tuning.hdev.hdev_templates import HDEV_HEADER, HDEV_TEMPLATE_CODE, HDEV_FOOTER
from param_tuning.utils import get_evias_experimts_path_for_hdev


def get_custom_hdev_pipeline_code(pipeline_name, dataset_path, param_lines, core_code):
    hdev_code = HDEV_HEADER

    # Dataset name and path
    hdev_code += "<l>dataset_name := '" + pipeline_name + "'</l>\n" + \
                 "<l>source_path := '" + get_evias_experimts_path_for_hdev() + dataset_path + "'</l>\n" + \
                 "<l>output_path := dataset_name + '/'</l>\n" + \
                 "<c></c>\n"

    hdev_code += HDEV_TEMPLATE_CODE

    for line in param_lines:
        hdev_code += line

    hdev_code += core_code

    hdev_code += HDEV_FOOTER

    return hdev_code
