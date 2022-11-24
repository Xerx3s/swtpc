import pandas as pd
from sklearn.model_selection import train_test_split

from floc_analyzer.scripts.modules.connectdb import connectdb
from floc_analyzer.scripts.modules.mlalgorithms import createpipeXGB as createpipeline
from floc_analyzer.scripts.modules.mlalgorithms import assess_pipeline, save_pipeline, load_pipeline
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
                self.dataset = self.dataset.query('surface_water == @sw & flocculant == @floc')
                self.dataset.drop(columns=["surface_water", "flocculant"], inplace=True)
                print(self.dataset)
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
    
    if load:
        pipe = load_pipeline(config.pipe_loadpath)
        print("pipe loaded.")
    else:
        pipe = createpipeline()
        pipe.fit(X_train.values, y_train)
        print("new pipe trained.")
    
    if printass:
        assess_pipeline(pipe, X_train, X_test, y_train, y_test)
        actualvpredicted, scores, evaluation = assess_pipeline(pipe, X_train, X_test, y_train, y_test)
        print(actualvpredicted)
        print(scores)
        print(evaluation)

    #return pipe, X_train, X_test, y_train, y_test
    return pipe

def outputprediction(inputvalues: list, pred_type: str, sw: str = None, floc: str = None, loadpipe: bool = True, printass: bool = False):
    #pipe, _, _, _, _ = trainorloadpipe(pred_type, loadpipe, printass)
    pipe = trainorloadpipe(pred_type, sw, floc, loadpipe, printass)
    return int(pipe.predict([inputvalues]))
    