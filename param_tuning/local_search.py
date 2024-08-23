import numpy as np

from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph
from param_tuning.hdev_manual.run_hdev_manual import get_manual_hdev_pipeline_bounds


def local_search(objective, bounds, n_iterations, step_size):
    # Initialize the best solution with a random point within the bounds
    best = bounds[:, 0] + np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
    best_eval = objective(best)
    scores = [best_eval]

    for i in range(n_iterations):
        # Take a step
        candidate = best + np.random.randn(len(bounds)) * step_size
        candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
        candidate_eval = objective(candidate)

        # Check if we should keep the new point
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)

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
