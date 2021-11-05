"""! @brief Experiment."""

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
    print("Hello world!")
    # signal.signal(signal.SIGINT, signal_handler)
    # Implement machine learning things here.
    # , model_executable_path, arguments
    #subprocess.call([
    #    model_executable_path +
    #    arguments
    #])