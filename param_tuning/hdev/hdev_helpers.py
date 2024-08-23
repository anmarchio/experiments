import math

import numpy as np

from param_tuning.hdev.hdev_function_lookup import HDEV_FUNCTION_LOOKUP
from param_tuning.hdev.hdev_templates import HDEV_HEADER, HDEV_FOOTER, HDEV_TEMPLATE_CODE

"""
Helper Functions for HDEV Code
"""


def extract_bounds_from_graph(graph):
    bounds = np.array
    bounds_identifiers = []
    """
    Only use the bounds that are represented by 
        INTEGERS or FLOATS, NOT strings (or e.g. struct elements).
    They are not as sensitive to the follow-up optimization and therefore banned.
    We only return a np array of continuous numbers for optimization.
    
    Instead, a set of parameters is placed at the beginning of the HDEV code to set the params each time;
    """
    for k in graph['pipeline'].keys():
        if k in HDEV_FUNCTION_LOOKUP.keys():
            tmp_bounds = HDEV_FUNCTION_LOOKUP[k]['bounds']
            for b in tmp_bounds.keys():
                if tmp_bounds[b] is not None:
                    if np.size(bounds) > 1:
                        bounds = np.append(bounds, np.array([list(tmp_bounds[b])]), axis=0)
                    else:
                        bounds = np.array([list(tmp_bounds[b])])
                    bounds_identifiers.append(b)

    return bounds, bounds_identifiers


def convert_params_to_hdev(graph: dict, params: np.array):
    _, bounds_identifiers = extract_bounds_from_graph(graph)
    hdev_output = ""

    i = 0
    for p in params:
        hdev_output += "<l>" + bounds_identifiers[i] + " := " + str(p) + "</l>\n"
        i += 1

    return hdev_output


def translate_graph_to_hdev(graph: dict, params: np.array = None):
    # HDEV xml style header
    hdev_output = HDEV_HEADER

    # Define source and output path for reading image
    # and writing results (binary images)
    hdev_output += "<l>source_path := '" + \
                   graph['training_path'].replace("\\", "/") + "/images'</l>\n"
    hdev_output += "<l>output_path := '" + \
                   graph['datetime'].strftime("%Y%m%d%H%M").replace("\\", "/") + "'</l>\n"
    hdev_output += HDEV_TEMPLATE_CODE

    if params is not None:
        hdev_output += convert_params_to_hdev(graph, params)

    # Decode pipeline and translate to hdev code
    # node by node from graph dict
    for k in graph['pipeline'].keys():
        hdev_output += get_main_function_hdev_code(k, graph['pipeline'][k])

    # Add the footer hdev code
    # to write results to binary image
    hdev_output += HDEV_FOOTER

    return hdev_output


def get_main_function_hdev_code(operator: str, params: np.array) -> str:
    """
    For every operator name we check for a special hdev translation
    and return it if found.
    if it is just a regular function found in HDEV_FUNCTION_LOOKUP
    it will be returned 'as is'.
    """
    hdev_code = ""

    raise ArithmeticError("!!INCOMPLETE CODE!!")

    if operator == 'Rectangle' or operator == 'Circle' or operator == 'Ellipse':
        hdev_code += generate_struct_hdev_line(operator, params)

    else:
        if operator in HDEV_FUNCTION_LOOKUP.keys():
            hdev_code += HDEV_FUNCTION_LOOKUP[operator]['hdev']
            i = 0
            for p in params.keys():
                # Reading the CGP generated parameter
                # hdev_output += graph['pipeline'][k][p]
                # Instead, use the simulated annealing parameters
                hdev_code += str(params[p])
                i += 1
                if i < len(params.keys()):
                    hdev_code += ", "

            hdev_code += ")</l>\n"

    return hdev_code


def generate_struct_hdev_line(struct_type: str, shape_params: []):
    """
    Returns hdev code to generate a special struct element of the sort
    Rectangle, Circle or Ellipse
    """
    struct_element_code = "<l>"
    if struct_type == "Rectangle":
        struct_element_code += "gen_rectangle1(StructElement, 0, 0, " + \
                              str(shape_params[0]) + ", " + \
                              str(shape_params[1]) + ")</l>\n"
    elif struct_type == "Circle":
        param1 = math.ceil(shape_params[0] + 1)
        param2 = math.ceil(shape_params[1] + 1)
        struct_element_code += "gen_circle(StructElement, " + \
                              str(param1) + ", " + \
                              str(param2) + ", " + \
                              str(shape_params[1]) + ")</l>\n"
    elif struct_type == "Ellipse":
        longer = shape_params[0]
        shorter = shape_params[1]
        if shorter > longer:
            tmp = shorter
            shorter = longer
            longer = tmp
        param1 = math.ceil(longer + 1)
        param2 = math.ceil(longer + 1)
        phi = 0
        struct_element_code += "gen_ellipse(StructElement, " + \
                              str(param1) + ", " + \
                              str(param2) + ", " + \
                              str(phi) + ", " + \
                              str(longer) + ", " + \
                              str(shorter) + ")</l>\n"
    else:
        struct_element_code += "</l>\n"

    return struct_element_code
