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
Default Path
"""
WDIR = os.path.join("C:\\", "dev", "experiments")

"""
Output Path for Subsequent Pipeline Optimization (SA, LS)
"""
HDEV_RESULTS_PATH = os.path.join(WDIR, "test")
PARAM_TUNING_RESULTS_PATH = os.path.join(HDEV_RESULTS_PATH, "param_tuning")
RESULTS_PATH = p_join(os.path.curdir, os.path.join(os.pardir, "scripts", "results"))
PARAM_TUNING_HDEV_MANUAL = os.path.join(PARAM_TUNING_RESULTS_PATH, "hdev_manual")

"""
Test Parameter Variables
"""
# TEST_EXPERIMENT_PATH = os.path.join(WDIR, "scripts", "results", "202302191650")
TEST_EXPERIMENT_PATH = os.path.join(WDIR, "scripts", "results", "202302021900")
TEST_SOURCE_JSON_PATH = os.path.join(TEST_EXPERIMENT_PATH, "source.json")
TEST_PIPELINE_TXT_PATH = os.path.join(TEST_EXPERIMENT_PATH, "Grid", "2", "pipeline.txt")
