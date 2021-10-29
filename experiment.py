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
def run(_config, model_executable_path, arguments):
    """Register signal handler."""
    signal.signal(signal.SIGINT, signal_handler)

    # Implement machine learning things here.
    subprocess.call([
        model_executable_path +
        arguments
    ])