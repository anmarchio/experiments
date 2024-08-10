import os

from os.path import join as p_join

"""
Variables for CGP experiment results
"""
# SPECIFIC_SOURCE_PATH = os.path.join("P:\\", "99 Austausch_TVöD", "mara", "Dissertation", "20230120results_dl2")
SPECIFIC_SOURCE_PATH = ""

# SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230329-163243data_arr.json")
# SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230509-025213data_arr.json")
# SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230512-151338data_arr.json")
SAMPLE_IMAGES_DIR_PATH = os.path.join("C:\\", "dev", "experiments", "data", "20230519-999data_arr_DEBUG.json")

"""
Parameter Tuning Variables
"""
experiments_path = os.path.join("C:\\", "dev", "experiments", "scripts", "results", "202302191650")
source_json_path = os.path.join(experiments_path, "source.json")
pipeline_txt_path = os.path.join(experiments_path, "Grid", "2", "pipeline.txt")

results_path = p_join(os.path.curdir, '../scripts/results')

HDEV_RESULT = os.path.join("C:\\", "dev", "experiments", "test")