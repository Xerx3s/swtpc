import pandas as pd
from sklearn.model_selection import train_test_split

from bsf_concept.scripts.modules.connectdb import connectdb
from bsf_concept.scripts.modules.mlalgorithms import createpipeXGB as createpipeline
from bsf_concept.scripts.modules.mlalgorithms import assess_pipeline, save_pipeline, load_pipeline
from bsf_concept.scripts.modules.pso import minimize
import bsf_concept.scripts.modules.config as config

class preparedataset:
    def __init__(self):
        raw = connectdb().bsfdatatodf()
        self.dataset = raw.append(raw) # Datengrundlage verdoppeln...
        
        """ wenn df["mean spalte"] leer dann aus min max werten berechnen
        self.dataset.loc[self.dataset["mean_grain_diameter"].isnull(),'mean_grain_diameter'] = (self.dataset["min_grain_diameter"] + self.dataset["max_grain_diameter"])/2
        self.dataset.loc[self.dataset["mean_flow"].isnull(),'mean_flow'] = (self.dataset["min_flow"] + self.dataset["max_flow"])/2
        self.dataset.loc[self.dataset["mean_pause"].isnull(),'mean_pause'] = (self.dataset["min_pause"] + self.dataset["max_pause"])/2 
        """
        
        self.dataset.drop(columns=["id", "material"], inplace=True)
        self.dataset.drop(columns=["initial_ecoli", "final_ecoli"], inplace=True)
        self.dataset.drop(columns=["min_grain_diameter", "max_grain_diameter", "min_flow", "max_flow", "min_pause", "max_pause"], inplace=True)
        self.target = ["final_turbidity"]

    def traintestset(self):
        y = self.dataset[self.target]
        self.dataset.drop(columns=self.target, inplace=True)
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, y,
                                                            test_size=config.test_dataset_size,
                                                            random_state=config.rand_state)
        return X_train, X_test, y_train, y_test

def trainorloadpipe(load: bool, printass: bool):
    X_train, X_test, y_train, y_test = preparedataset().traintestset()

    lb = X_train.min()
    ub = X_train.max()
    bounds = {}
    for index,value in lb.items():
        bounds[index] = [value, ub[index]+0.1]

    if load:
        pipe = load_pipeline("bsf_concept/data/pipe_bsf.dump")
        print("pipe loaded.")
    else:
        pipe = createpipeline()
        pipe.fit(X_train.values, y_train)
        save_pipeline(pipe, "bsf_concept/data/pipe_bsf.dump")
        print("new pipe trained and saved.")
    
    if printass:
        actualvpredicted, scores, evaluation = assess_pipeline(pipe, X_train, X_test, y_train, y_test)
        print(
            "\nPrediction Test with test dataset\n",
            "actual vs. predicted output:\n",
            actualvpredicted,
            '\nnumber of rows: %d' %(scores["rows"]),
            "\nTrainings-Score: %.4f" %(scores["train_score"]),
            "\nTest-Score: %.4f" %(scores["test_score"]),
            "\nUsed input features: ", (scores["used_features"]),
            '\nEvaluation report:',
            "\nRMSE: %.2f" %(evaluation["rmse"]),
            "\nMAE: %.2f" %(evaluation["mae"]))

    #return pipe, X_train, X_test, y_train, y_test
    return pipe, bounds

def outputprediction(inputvalues: list, loadpipe: bool = True, printass: bool = False):
    pipe, _ = trainorloadpipe(loadpipe, printass)
    prediction = round(float(pipe.predict([inputvalues])),1)
    #print("prediction: " + prediction)
    return prediction
    
def inputoptimization(bounds: dict, loadpipe: bool = True, printass: bool = False):
    """
        Bounds need to be dict of type {param: [min, max]}.\n
        Keys for param: initial_turbidity, diameter, material_height, mean_grain_diameter, mean_flow, mean_pause, time_schmutzdecke.
    """
    pipe, _ = trainorloadpipe(loadpipe, printass)
    output, best_param = minimize(pipe=pipe, bounds=bounds)

    return output, best_param