import numpy as np

from param_tuning.algorithm_step import perturb, LS_N_ITERATIONS, LS_STEP_SIZE
from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds, get_initial_state_by_pipeline_name
from param_tuning.simulated_annealing import params_to_str
from param_tuning.utils import write_header_to_log, write_log, format_line
from settings import PARAM_TUNING_HDEV_MANUAL


# analogue to Example Simulated Annealing step
def local_search_step(current_state, bounds, step_size):
    new_state = []
    for i, value in enumerate(current_state):
        new_value = perturb(value, bounds[i], step_size)
        new_state.append(new_value)
    return np.array(new_state)


def local_search(pipeline_name, graph, objective, bounds, n_iterations, step_size):
    # Initialize the best solution with a random point within the bounds
    best = np.array

    if graph is None:
        best = get_initial_state_by_pipeline_name(pipeline_name)
    else:
        best = graph['bounds']

    best_eval = objective(pipeline_name, graph, best)

    curr, curr_eval = best, best_eval
    scores = [best_eval]

    write_header_to_log(pipeline_name)
    write_log(pipeline_name, format_line(-1, -best_eval, params_to_str(curr), "ls", f"step:{step_size}", pipeline_name))

    for i in range(n_iterations):
        # Take a step
        # candidate = best + np.random.randn(len(bounds)) * step_size
        # candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
        # candidate_eval = objective(candidate)
        candidate = local_search_step(curr, bounds, step_size)
        candidate_eval = objective(pipeline_name, graph, candidate)

        # Check if we should keep the new point
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)

        output = format_line(i, -best_eval, params_to_str(candidate), "ls", f"step:{step_size}", pipeline_name)
        print(output)
        write_log(PARAM_TUNING_HDEV_MANUAL, pipeline_name, output)

    return best, best_eval


def run_local_search(pipeline_name, graph, objective, manual=True):
    bounds = np.array

    if manual:
        bounds = get_manual_hdev_pipeline_bounds(pipeline_name)
    else:
        bounds, _ = extract_bounds_from_graph(graph)

    best_params, best_score = local_search(pipeline_name, graph, objective, bounds, LS_N_ITERATIONS, LS_STEP_SIZE)

    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
