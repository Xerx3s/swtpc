import pandas as pd
from sklearn.model_selection import train_test_split

from floc_analyzer.scripts.modules.connectdb import connectdb
from floc_analyzer.scripts.modules.mlalgorithms import createpipeXGB as createpipeline
from floc_analyzer.scripts.modules.mlalgorithms import assess_pipeline, save_pipeline, load_pipeline
from floc_analyzer.scripts.modules.pso import minimize
import floc_analyzer.scripts.modules.config as config

class preparedataset:
    def __init__(self, pred_type: str, sw: str, floc: str):
        self.pred_type = pred_type
        try:
            if self.pred_type == "ec":
                self.dataset = connectdb().flocdataEC()
                self.target = ["final_EC"]
            elif self.pred_type == "ph":
                self.dataset = connectdb().flocdatapH()
                self.target = ["final_pH"]
            elif self.pred_type == "tur":
                self.dataset = connectdb().flocdataTur()
                #self.dataset = self.dataset.query('surface_water == @sw & flocculant == @floc')
                self.dataset.drop(columns=["surface_water", "flocculant"], inplace=True)
                self.target = ["final_turbidity"]
        except:
            print("wrong prediction type")

    def traintestset(self):
        y = self.dataset[self.target]
        self.dataset.drop(columns=self.target, inplace=True)
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, y,
                                                            test_size=config.test_dataset_size,
                                                            random_state=config.rand_state)
        return X_train, X_test, y_train, y_test

def trainorloadpipe(pred_type: str, sw: str, floc: str, load: bool, printass: bool):
    X_train, X_test, y_train, y_test = preparedataset(pred_type=pred_type, sw=sw, floc=floc).traintestset()

    lb = X_train.min()
    ub = X_train.max()
    bounds = {}
    for index,value in lb.items():
        bounds[index] = [value, ub[index]+0.1]

    if load:
        if pred_type == "ph":
            pipe = load_pipeline("floc_analyzer/data/pipe_ph.dump")
        elif pred_type == "ec":
            pipe = load_pipeline("floc_analyzer/data/pipe_ec.dump")
        elif pred_type == "tur":
            pipe = load_pipeline("floc_analyzer/data/pipe_tur.dump")
        print("pipe loaded.")
    else:
        pipe = createpipeline()
        pipe.fit(X_train.values, y_train)
        if pred_type == "ph":
            save_pipeline(pipe, "floc_analyzer/data/pipe_ph.dump")
        elif pred_type == "ec":
            save_pipeline(pipe, "floc_analyzer/data/pipe_ec.dump")
        elif pred_type == "tur":
            save_pipeline(pipe, "floc_analyzer/data/pipe_tur.dump")
        print("new pipe trained and saved.")
    
    if printass:
        actualvpredicted, scores, evaluation = assess_pipeline(pipe, X_train, X_test, y_train, y_test)
        print(
            "\nPrediction Test (%s) with test dataset\n" %(pred_type),
            "actual vs. predicted output:\n",
            actualvpredicted,
            '\nnumber of rows: %d' %(scores["rows"]),
            "\nTrainings-Score: %.4f" %(scores["train_score"]),
            "\nTest-Score: %.4f" %(scores["test_score"]),
            "\nUsed input features: ", (scores["used_features"]),
            '\nEvaluation report:',
            "\nRMSE: %.2f" %(evaluation["rmse"]),
            "\nMAE: %.2f" %(evaluation["mae"]),
            "\nMAPE: %.2f" %(evaluation["mape"]),
            '\nAccuracy: %.2f'%((100-evaluation["mape"])))

    #return pipe, X_train, X_test, y_train, y_test
    return pipe, bounds

def outputprediction(inputvalues: list, pred_type: str, sw: str = None, floc: str = None, loadpipe: bool = True, printass: bool = False):
    #pipe, _, _, _, _ = trainorloadpipe(pred_type, loadpipe, printass)
    pipe, _ = trainorloadpipe(pred_type, sw, floc, loadpipe, printass)
    prediction = round(float(pipe.predict([inputvalues])),1)
    #print("prediction: " + prediction)
    return prediction
    
def inputoptimization(bounds: dict, pred_type: str, sw: str = None, floc: str = None, loadpipe: bool = True, printass: bool = False):
    """
        Bounds need to be dict of type {param: [min, max]}.\n
        Keys for param: initial_pH, initial_EC, initial_turbidity, floc_concentration, floc_saline_Molarity
        floc_dose, floc_cactus_share, stirring_speed_coagulation_phase, duration_coagulation_phase, stirring_speed_flocculation_phase, duration_flocculation_phase, duration_sedimentation_phase
    """
    pipe, _ = trainorloadpipe(pred_type, sw, floc, loadpipe, printass)
    output, best_param = minimize(pipe=pipe, pred_type=pred_type, bounds=bounds)

    return output, best_param