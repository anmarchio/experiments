"""! @brief Experiment."""
import os
import signal
import subprocess
import sys

from sacred import Experiment
from util.config import Config

global_config = Config()
ex = Experiment()


def signal_handler(sig, frame):
    """Abort training when interrupt from keyboard (CTRL + C) occurs."""
    print('sig: ', str(sig))
    print('frame: ', str(frame))
    print("\n\nAborting...")
    sys.exit(0)


@ex.main
def run(_config):
    """Register signal handler."""
    signal.signal(signal.SIGINT, signal_handler)
    print("Hello world!")
    # Implement machine learning things here.

    model_executable_path = os.path.join(
        "C:\\",
        "dev",
        "optimization",
        "Optimization.Commandline",
        "bin",
        "Debug",
        "Optimization.Commandline.exe"
    )

    # train_data_parent_dir = r"Q:\5 Fachbereiche\03 OPM\ReferenzSet\EXIST\out"
    # val_data_parent_dir = r"Q:\5 Fachbereiche\03 OPM\ReferenzSet\EXIST\out_lbl"
    train_data_parent_dir = os.path.join("C:\\", "Users", "mara_c10", "Desktop", "ReferenzSet", "EXIST", "out")
    val_data_parent_dir = os.path.join("C:\\", "Users", "mara_c10", "Desktop", "ReferenzSet", "EXIST", "out_lbl")

    arguments = " batch --backend=halcon " \
                "--runs=5 " \
                "--train-data-dir=" \
                + train_data_parent_dir + " " + \
                "--val-data-dir= " \
                + val_data_parent_dir + " " +  \
                "--generations=200"

    subprocess.call([
        model_executable_path +
        arguments
    ])