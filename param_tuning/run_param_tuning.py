import sys
import os

import numpy as np

from param_tuning.local_search import run_local_search
from param_tuning.simulated_annealing import run_simulated_annealing
from read_dot import read_dot_file, parse_dot


def run_pipeline(amplitude, threshold_value):
    raise NotImplementedError


def objective(params):
    amplitude, threshold_value = params
    # Run the pipeline with given parameters and evaluate performance
    # Assuming run_pipeline returns a performance metric like accuracy
    performance = run_pipeline(amplitude, threshold_value)
    return -performance  # Minimize negative performance to maximize performance

def main() -> int:
    """
    Read the filter pipeline
    """
    # File path to the dot content
    file_path = os.path.join("C:\\","dev","experiments","scripts","results","202302191650","Grid","2", "pipeline.txt")
    # Read the dot content from the file
    dot_content = read_dot_file(file_path)
    # Parse the dot content
    nodes, edges = parse_dot(dot_content)
    # Print the nodes
    for node in nodes.values():
        print(node)
    # Optionally, print the edges
    print("Edges:")
    for edge in edges:
        print(edge)

    """
    Simulated Annealing
    """
    # Define the parameter bounds: [amplitude_bounds, threshold_bounds]
    bounds = np.array([[-128, 128], [0, 255]])
    sa_best_params0, sa_best_params1, sa_best_score = run_simulated_annealing(bounds)
    write_to_file(RESULT_PATH, 'sa', sa_best_params0, sa_best_params1, sa_best_score)
    """
    Local Search
    """
    ls_best_params0, ls_best_params1, ls_best_score = run_local_search(bounds)
    write_to_file(RESULT_PATH, 'ls', ls_best_params0, ls_best_params1, ls_best_score)

    """
    Write Latex
    """
    print_tex(RESULT_PATH)
    """
    file_path (source) | Algorithm | sa_best_params0 | sa_best_params1 | sa_best_score
    """

if __name__ == '__main__':
    main()
    # next section explains the use of sys.exit
    sys.exit()