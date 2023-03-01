import numpy as np
from pyswarms.single.global_best import GlobalBestPSO
from sklearn.pipeline import Pipeline

def create_objective_function(pipe: Pipeline):
    def objective_function(input_param):
        output = pipe.predict(input_param)
        return output
    return objective_function

def minimize(pipe: Pipeline, bounds: dict):
    particles = 50
    iterations = 100
    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

    objective_function = create_objective_function(pipe=pipe)

    bounds_tuple = (
        np.array([
            bounds["diameter"][0],
            bounds["material_height"][0],
            bounds["mean_grain_diameter"][0],
            bounds["mean_flow"][0],
            bounds["mean_pause"][0],
            bounds["time_schmutzdecke"][0],
            bounds["initial_turbidity"][0],
        ]),
        np.array([
            bounds["diameter"][1],
            bounds["material_height"][1],
            bounds["mean_grain_diameter"][1],
            bounds["mean_flow"][1],
            bounds["mean_pause"][1],
            bounds["time_schmutzdecke"][1],
            bounds["initial_turbidity"][1],
        ]),
    )
    optimizer = GlobalBestPSO(n_particles=particles, dimensions=7, options=options, bounds=bounds_tuple)
    
    output, best_param = optimizer.optimize(objective_function, iters=iterations)
    
    if output < 0:
        output = 0

    best_param = [0 if np.isnan(param) else param for param in best_param]

    return output, best_param