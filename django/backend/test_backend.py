import numpy as np

from floc_analyzer.scripts.new_main import outputprediction, trainorloadpipe
from floc_analyzer.scripts.modules.pso import create_objective_function, minimize

class TestPrediction:
    def test_prediction_EC(self):
        #input: iEC, fcon, fsalM, fdose, fvol, fsalcon
        input_param = [400, 20, 0.3, 200]
        input_param.append(input_param[3]/input_param[1]),
        input_param.append(input_param[4]*input_param[2])
        assert outputprediction(
            inputvalues=input_param,
            pred_type="ec",
            loadpipe=False) > 600

    def test_prediction_pH(self):
        #input: ipH, fcon, fsalM, fdose
        input_param = [400, 20, 0.3, 200]
        assert outputprediction(
            inputvalues=input_param,
            pred_type="ph",
            loadpipe=False) < 9

    def test_prediction_tur(self):
        #input: ipH, iEC, itur, fsalM, fdose, fcactus, sscp, dcp, ssfp, dfp, dsp
        input_param = [8.5, 400, 130, 0.3, 200, 0, 100, 1, 20, 15, 45]
        assert outputprediction(
            inputvalues=input_param,
            pred_type="tur",
            loadpipe=False) < 100
    
class TestOptimizer:
    def test_optimizer_EC(self):
        pred_type = "ec"
        
        pipe, bounds = trainorloadpipe(pred_type=pred_type, sw="model suspension", floc="Moringa", load=False, printass=False)

        objective_function = create_objective_function(pipe=pipe)
        output, best_param = minimize(objective_function=objective_function, pred_type=pred_type, bounds=bounds)

        assert output > 400
        
    def test_optimizer_pH(self):
        pred_type = "ph"

        pipe, bounds = trainorloadpipe(pred_type=pred_type, sw="model suspension", floc="Moringa", load=False, printass=False)

        objective_function = create_objective_function(pipe=pipe)
        output, best_param = minimize(objective_function=objective_function, pred_type=pred_type, bounds=bounds)

        assert output < 9

    def test_optimizer_tur(self):
        pred_type = "tur"

        pipe, bounds = trainorloadpipe(pred_type=pred_type, sw="model suspension", floc="Moringa", load=False, printass=False)
        
        objective_function = create_objective_function(pipe=pipe)
        output, best_param = minimize(objective_function=objective_function, pred_type=pred_type, bounds=bounds)

        assert output < 20