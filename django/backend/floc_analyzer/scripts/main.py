from typing import Tuple
import numpy as np
import flocculation_analysis.modules.config as config
from flocculation_analysis.modules.datahandling import importdata, finalizedata
from flocculation_analysis.modules.mlalgorithms import createpipeXGB as createpipeline
from flocculation_analysis.modules.mlalgorithms import save_pipeline, load_pipeline, assess_pipeline
from flocculation_analysis.modules.optimizers import optimize, optimizewithboders
import pandas as pd

# Als Klasse definieren, damit Verbindung zur Datenbank nur einmal aufgebaut werden muss.

def trainorloadpipe(load: bool = True, printass: bool = False):
    # create train-test-set
    X_train, X_test, y_train, y_test = importdata(config.imp_path)
    
    if load:
        pipe = load_pipeline(config.pipe_loadpath)
        print("pipe loaded.")
    else:
        pipe = createpipeline()
        pipe.fit(X_train.values, y_train)
        print("new pipe trained.")
    
    if printass: printassessment(pipe, X_train, X_test, y_train, y_test)

    return pipe, X_train, X_test, y_train, y_test

def printassessment(pipe, X_train, X_test, y_train, y_test):
    """
    Show test and predicted data, model scores and evaluation report in terminal.
    """
    actualvpredicted, scores, evaluation = assess_pipeline(pipe, X_train, X_test, y_train, y_test)
    print("\n Prediction Test with test dataset")
    print("actual vs. predicted output:")
    print(actualvpredicted)
    print('\nnumber of rows: %d' %(scores["rows"]))
    print("Trainings-Score: %.4f" %(scores["train_score"]))
    print("Test-Score: %.4f" %(scores["test_score"]))
    print("Used input features: ", (scores["used_features"]))
    print('\nEvaluation report:')
    print ("RMSE: %.2f" %(evaluation["rmse"]))
    print ("MAE: %.2f" %(evaluation["mae"]))
    print ("MAPE: %.2f" %(evaluation["mape"]))
    print('Accuracy: %.2f'%((100-evaluation["mape"])))
    
    save_pipeline(pipe, config.pipe_savepath)
    print("Pipe saved")

def printoptimalresults():
    pipe, X_train, _, _, _ = trainorloadpipe()

    # optimal input features and predicted output
    optimal_pars = optimize(pipe, X_train)
    df_optimal_pars = pd.DataFrame.from_dict(optimal_pars, orient="index")
    out_optimal_pars = finalizedata(df_optimal_pars)
    print('\noptimized input features:')
    print(out_optimal_pars[0])
    optimal_prediction = pipe.predict([df_optimal_pars[0].tolist()])
    ftur = optimal_pars["itur"]-optimal_pars["itur"]*optimal_prediction[0][0]
    if ftur < 0: ftur = 0
    print("\npredicted performance with optimal input features: %0.2f" % optimal_prediction[0][0])
    print("predicted final turbidity: %d NTU" % ftur)
    print("predicted final pH at %.1f; predicted final EC at %d µS/cm" % (optimal_prediction[0][1], optimal_prediction[0][2]))

    save_pipeline(pipe, config.pipe_savepath)
    print("Pipe saved")

def predictfromvalues(loadpipe: bool, printass: bool, inputvalues: list):
    pipe, _, _, _, _ = trainorloadpipe(loadpipe, printass)
    result = pipe.predict([inputvalues])
    result[0][0] = (1 - result[0][0]) * inputvalues[2]
    rounded = np.around(result[0], 2)
    return rounded

def predictnovalues(loadpipe: bool, printass: bool, inputvalues: list):
    pipe, X_train, _, _, _ = trainorloadpipe(loadpipe, printass)
    optimal_pars = optimizewithboders(pipe, X_train, inputvalues)
    df_optimal_pars = pd.DataFrame.from_dict(optimal_pars, orient="index")
    result = pipe.predict([df_optimal_pars[0].tolist()])
    result[0][0] = (1 - result[0][0]) * inputvalues["itur"]
    rounded = np.around(result[0], 2)
    return rounded, df_optimal_pars[0]