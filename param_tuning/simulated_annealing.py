from decimal import Decimal

import numpy as np

from param_tuning.algorithm_step import params_to_str, perturb, SA_N_ITERATIONS, SA_COOLING_RATE, SA_TEMP
from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph
from param_tuning.run_hdev_manual import get_initial_state_by_pipeline_name, get_manual_hdev_pipeline_bounds
from param_tuning.utils import write_header_to_log, write_log, format_line
from settings import PARAM_TUNING_HDEV_MANUAL


# Example Simulated Annealing step
def simulated_annealing_step(current_state, bounds, temperature):
    new_state = []
    for i, value in enumerate(current_state):
        new_value = perturb(value, bounds[i], temperature)
        new_state.append(new_value)
    return np.array(new_state)


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

    write_header_to_log(pipeline_name)
    write_log(pipeline_name, format_line(-1, -best_eval, params_to_str(curr),
                                         f"cooling:{cooling_rate},temp:{temp}", "sa", pipeline_name))

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

        output = format_line(i, -best_eval, params_to_str(candidate), "sa",
                             f"cooling:{cooling_rate},temp:{temp}", pipeline_name)
        print(output)
        write_log(PARAM_TUNING_HDEV_MANUAL, pipeline_name, output)

        temp *= cooling_rate

    return best, best_eval


def run_simulated_annealing(pipeline_name, graph, objective, manual: bool = True):
    bounds = []

    if manual:
        bounds = get_manual_hdev_pipeline_bounds(pipeline_name)
    else:
        bounds, _ = extract_bounds_from_graph(graph)

    #try:
    best_params, best_score = simulated_annealing(pipeline_name,
                                                  graph,
                                                  objective,
                                                  bounds,
                                                  SA_N_ITERATIONS,
                                                  SA_COOLING_RATE,
                                                  SA_TEMP)

    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
    # except Exception as e:
    #    print(e)
    #    write_to_log(pipeline_name, str(e))
    #    return [], [], 0.0
