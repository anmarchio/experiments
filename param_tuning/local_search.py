import numpy as np


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

def run_local_search(bounds):
    # Run Local Search
    n_iterations = 1000
    step_size = 0.1
    best_params, best_score = local_search(objective, bounds, n_iterations, step_size)
    print(f"Optimized parameters: amplitude={best_params[0]}, threshold={best_params[1]}")
    print(f"Best performance: {-best_score}")
    return best_params[0], best_params[1], best_score
