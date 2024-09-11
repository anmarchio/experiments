import random

from numpy import int32

"""
Simulated Annealing Default Parameters
"""
SA_N_ITERATIONS = 30
SA_COOLING_RATE = 0.9
SA_TEMP = 10.0


"""
Local Search Default Parameters
"""
LS_N_ITERATIONS = 30
LS_STEP_SIZE = 0.1



def perturb(value, bound, temperature):
    try:
        if isinstance(value, int):
            value = int(value)
        if isinstance(value, float):
            value = float(value)
    except ValueError:
        print("Conversion Error in Perturb.")

    if len(bound) == 1:
        return value
    if isinstance(value, str):
        # NO: For strings, randomly choose a different string from the list
        options = [opt for opt in bound if opt != value]
        return random.choice(options)
        # just return string as is
        #return value
    elif isinstance(value, (int, int32, float)):
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


def params_to_str(values):
    params_str = ""
    for v in values:
        params_str += str(v) + ", "
    return params_str
