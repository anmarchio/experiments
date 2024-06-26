from scipy.optimize import differential_evolution

# Define the objective function
def objective(params):
    amplitude, threshold_value = params
    # Run the pipeline with given parameters and evaluate performance
    # Assuming run_pipeline returns a performance metric like accuracy
    performance = run_pipeline(amplitude, threshold_value)
    return -performance  # Minimize negative performance to maximize performance

# Parameter bounds: [amplitude_bounds, threshold_bounds]
bounds = [(-128, 128), (0, 255)]

# Perform Particle Swarm Optimization
result = differential_evolution(objective, bounds, strategy='best1bin', maxiter=100, popsize=15)

# Best parameters
best_amplitude, best_threshold_value = result.x
print(f"Optimized parameters: amplitude={best_amplitude}, threshold={best_threshold_value}")
