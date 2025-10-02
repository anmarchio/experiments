"""
env_var.py

Global system environment variables
"""
import os

from settings import WDIR

DEV_MODE = True

SQLITE_TEST_PATH = "experiments_test.db"
#SQLITE_PATH = os.path.join(WDIR, "api", "experiments.db")
SQLITE_PATH = os.path.join(WDIR, "api", "20241120experiments.db")
