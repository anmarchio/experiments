import numpy as np

from param_tuning.hdev.hdev_helpers import extract_bounds_from_graph


def simulated_annealing(graph, objective, bounds, n_iterations, step_size, temp):
    # Initialize the best solution with a random point within the bounds
    best = bounds[:, 0] + np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])

    best_eval = objective(graph, best)
    curr, curr_eval = best, best_eval
    scores = [best_eval]

    for i in range(n_iterations):
        # Take a step
        candidate = curr + np.random.randn(len(bounds)) * step_size
        candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
        candidate_eval = objective(graph, candidate)

        # Check if we should keep the new point
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)

        # Calculate the difference between evaluations
        diff = candidate_eval - curr_eval
        t = temp / float(i + 1)

        # Metropolis acceptance criterion
        metropolis = np.exp(-diff / t)
        if diff < 0 or np.random.rand() < metropolis:
            curr, curr_eval = candidate, candidate_eval

    return best, best_eval


def run_simulated_annealing(graph, objective):
    n_iterations = 1000
    step_size = 0.1
    temp = 10.0

    bounds, _ = extract_bounds_from_graph(graph)

    best_params, best_score = simulated_annealing(graph, objective, bounds, n_iterations, step_size, temp)

    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
