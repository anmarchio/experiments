import datetime
import random
from decimal import Decimal

import numpy as np

from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds, get_initial_state_by_pipeline_name
from param_tuning.utils import write_to_log


def perturb(value, bound, temperature):
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
            delta = (bound[1] - bound[0]) * temperature * (random.random() - 0.5)
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


# Example Simulated Annealing step
def simulated_annealing_step(current_state, bounds, temperature):
    new_state = []
    for i, value in enumerate(current_state):
        new_value = perturb(value, bounds[i], temperature)
        new_state.append(new_value)
    return np.array(new_state)


def params_to_str(values):
    params_str = ""
    for v in values:
        params_str += str(v) + ", "
    return params_str


def simulated_annealing(pipeline_name, graph, objective, bounds, n_iterations, cooling_rate, temp):
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
                 f"\n{'-' * 20}\nDataset: {pipeline_name}, SimAnn MCC, {datetime.datetime.now()}\n{'-' * 20}\n")
    for i in range(n_iterations):
        # Take a step
        # candidate = curr + np.random.randn(len(bounds)) * step_size
        # candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
        candidate = simulated_annealing_step(curr, bounds, temp)
        candidate_eval = objective(pipeline_name, graph, candidate)

        # Check if we should keep the new point
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)

        # Calculate the difference between evaluations
        diff = Decimal(candidate_eval) - Decimal(curr_eval)
        t = Decimal(temp) / Decimal(i + 1)

        # Metropolis acceptance criterion
        metropolis = np.exp(Decimal(-diff) / Decimal(t))
        if diff < 0 or np.random.rand() < metropolis:
            curr, curr_eval = candidate, candidate_eval

        output = f"Iteration: {i}, Temp: {temp}, Performance: {-best_eval}\n"
        output += f"\tParameters: {params_to_str(candidate)}\n"
        print(output)
        write_to_log(pipeline_name, output)

        temp *= cooling_rate

    return best, best_eval


def run_simulated_annealing(pipeline_name, graph, objective, manual: bool = True):
    n_iterations = 1000
    cooling_rate = 0.9
    temp = 10.0

    bounds = []

    if manual:
        bounds = get_manual_hdev_pipeline_bounds(pipeline_name)
    else:
        bounds, _ = extract_bounds_from_graph(graph)

    # try:
    best_params, best_score = simulated_annealing(pipeline_name,
                                                  graph,
                                                  objective,
                                                  bounds,
                                                  n_iterations,
                                                  cooling_rate,
                                                  temp)

    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
    # except Exception as e:
    #    print(e)
    #    write_to_log(pipeline_name, str(e))
    #    return [], [], 0.0
