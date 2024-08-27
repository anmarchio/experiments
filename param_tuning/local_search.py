import random
import numpy as np

from datetime import datetime

from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds, get_initial_state_by_pipeline_name
from param_tuning.simulated_annealing import params_to_str
from param_tuning.utils import write_to_log


def perturb(value, bound, step_size):
    try:
        value = int(value)
    except ValueError:
        print("Not int")

        # If that fails, try to convert the string to a float
    try:
        value = float(value)
    except ValueError:
        print("Not float")

    if len(bound) == 1:
        return value
    if isinstance(value, str):
        # NO: For strings, randomly choose a different string from the list
        options = [opt for opt in bound if opt != value]
        return random.choice(options)
        # just return string as is
        #return value
    elif isinstance(value, (int, float)):
        if len(bound) == 2:
            # For a range, slightly adjust the value within the bounds
            delta = (bound[1] - bound[0]) * step_size * (random.random() - 0.5)
            new_value = value + delta
            return max(min(new_value, bound[1]), bound[0])  # Ensure within bounds
        else:
            # For discrete numeric values, find the closest match
            closest_value = min(bound, key=lambda x: abs(x - value))
            idx = bound.index(closest_value)

            # Select a neighboring value
            if random.random() > 0.5 and idx < len(bound) - 1:
                return bound[idx + 1]
            elif idx > 0:
                return bound[idx - 1]
            return bound[idx]


# analogue to Example Simulated Annealing step
def local_search_step(current_state, bounds, step_size):
    new_state = []
    for i, value in enumerate(current_state):
        new_value = perturb(value, bounds[i], step_size)
        new_state.append(new_value)
    return np.array(new_state)


#def local_search(objective, bounds, n_iterations, step_size):
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

    write_to_log(pipeline_name,
                 f"\n{'-' * 20}\nDataset: {pipeline_name}, SimAnn MCC, {datetime.now()}\n{'-' * 20}\n")

    for i in range(n_iterations):
        # Take a step
        #candidate = best + np.random.randn(len(bounds)) * step_size
        # candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
        # candidate_eval = objective(candidate)
        candidate = local_search_step(curr, bounds, step_size)
        candidate_eval = objective(pipeline_name, graph, candidate)

        # Check if we should keep the new point
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)

        output = f"Iteration: {i}, Performance: {-best_eval}\n"
        output += f"\tParameters: {params_to_str(candidate)}\n"
        print(output)
        write_to_log(pipeline_name, output)

    return best, best_eval


def run_local_search(pipeline_name, graph, objective, manual = True):
    # Run Local Search
    n_iterations = 1000
    step_size = 0.1

    bounds = np.array

    if manual:
        bounds = get_manual_hdev_pipeline_bounds(pipeline_name)
    else:
        bounds, _ = extract_bounds_from_graph(graph)

    best_params, best_score = local_search(pipeline_name, graph, objective, bounds, n_iterations, step_size)

    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
