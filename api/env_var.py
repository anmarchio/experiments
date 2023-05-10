"""
env_var.py

Global system environment variables
"""
import os

DEV_MODE = True

SQLITE_TEST_PATH = "experiments_test.db"
SQLITE_PATH = os.path.join("experiments.db")
