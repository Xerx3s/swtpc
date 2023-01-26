import numpy as np
from pyswarms.single.global_best import GlobalBestPSO
from sklearn.pipeline import Pipeline

def create_objective_function(pipe: Pipeline):
    def objective_function(input_param):
        output = pipe.predict(input_param)
        return output
    return objective_function

def minimize(objective_function, pred_type: str, bounds: dict):
    particles = 50
    iterations = 100
    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

    if pred_type == "ec":
        bounds_tuple = (
            np.array([
                bounds["initial_EC"][0],
                bounds["floc_concentration"][0],
                bounds["floc_saline_Molarity"][0],
                bounds["floc_dose"][0],
                bounds["floc_dose"][0]/bounds["floc_concentration"][0],
                bounds["floc_dose"][0]/bounds["floc_concentration"][0]*bounds["floc_saline_Molarity"][0]
            ]),
            np.array([
                bounds["initial_EC"][1],
                bounds["floc_concentration"][1],
                bounds["floc_saline_Molarity"][1],
                bounds["floc_dose"][1],
                bounds["floc_dose"][1]/bounds["floc_concentration"][1],
                bounds["floc_dose"][1]/bounds["floc_concentration"][1]*bounds["floc_saline_Molarity"][1]
            ]),
        )
        optimizer = GlobalBestPSO(n_particles=particles, dimensions=6, options=options, bounds=bounds_tuple)
    elif pred_type == "ph":
        bounds_tuple = (
            np.array([
                bounds["initial_pH"][0],
                bounds["floc_concentration"][0],
                bounds["floc_saline_Molarity"][0],
                bounds["floc_dose"][0]
            ]),
            np.array([
                bounds["initial_pH"][1],
                bounds["floc_concentration"][1],
                bounds["floc_saline_Molarity"][1],
                bounds["floc_dose"][1]
            ]),
        )
        optimizer = GlobalBestPSO(n_particles=particles, dimensions=4, options=options, bounds=bounds_tuple)
    elif pred_type == "tur":
        bounds_tuple = (
            np.array([
                bounds["initial_pH"][0],
                bounds["initial_EC"][0],
                bounds["initial_turbidity"][0],
                bounds["floc_saline_Molarity"][0],
                bounds["floc_dose"][0],
                bounds["floc_cactus_share"][0],
                bounds["stirring_speed_coagulation_phase"][0],
                bounds["duration_coagulation_phase"][0],
                bounds["stirring_speed_flocculation_phase"][0],
                bounds["duration_flocculation_phase"][0],
                bounds["duration_sedimentation_phase"][0]
            ]),
            np.array([
                bounds["initial_pH"][1],
                bounds["initial_EC"][1],
                bounds["initial_turbidity"][1],
                bounds["floc_saline_Molarity"][1],
                bounds["floc_dose"][1],
                bounds["floc_cactus_share"][1],
                bounds["stirring_speed_coagulation_phase"][1],
                bounds["duration_coagulation_phase"][1],
                bounds["stirring_speed_flocculation_phase"][1],
                bounds["duration_flocculation_phase"][1],
                bounds["duration_sedimentation_phase"][1]
            ]),
        )
        optimizer = GlobalBestPSO(n_particles=particles, dimensions=11, options=options, bounds=bounds_tuple)
    
    return optimizer.optimize(objective_function, iters=iterations)
