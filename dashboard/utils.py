import json

import numpy as np


def read_file_and_return_norm_dict(file_name: str) -> {}:
    f = open(file_name, 'r')
    norm_arr_dict_list = json.load(f)
    f.close()
    return norm_arr_dict_list
