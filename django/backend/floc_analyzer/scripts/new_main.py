import pandas as pd
from sklearn.model_selection import train_test_split

from floc_analyzer.scripts.modules.connectdb import dbflocdatatodf
from floc_analyzer.scripts.modules.mlalgorithms import createpipeXGB as createpipeline
from floc_analyzer.scripts.modules.mlalgorithms import assess_pipeline, save_pipeline, load_pipeline
import floc_analyzer.scripts.modules.config as config

def trainorloadpipe(load: bool, printass: bool):
    # import dataset from db.
    dataset = dbflocdatatodf()

    # filter dataset before usage. (drop columns for prediction of fpH and fEC)

    # prepare dataset. isolate then drop target column.
    dataset.drop(columns=["cal_fEC", "d_EC"], inplace=True)
    target = ["fEC"]
    y = dataset[target]
    dataset.drop(columns=target, inplace=True)

    # split dataset into training and validation datasets
    X_train, X_test, y_train, y_test = train_test_split(dataset, y,
                                                        test_size=config.test_dataset_size,
                                                        random_state=config.rand_state)
    
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

    return pipe, X_train, X_test, y_train, y_test

def predictfromvalues(inputvalues: list, loadpipe: bool = True, printass: bool = False):
    pipe, _, _, _, _ = trainorloadpipe(loadpipe, printass)
    result = pipe.predict([inputvalues])
    result[0][0] = (1 - result[0][0]) * inputvalues[2]
    rounded = np.around(result[0], 2)
    return rounded