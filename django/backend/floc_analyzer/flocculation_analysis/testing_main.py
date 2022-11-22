import modules.config as config
import pyodbc
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
#from sklearn.multioutput import MultiOutputRegressor

class db_connection:

    def __init__(self, path: str = config.db_path):
            if self.checkdriver():
                print("Access Driver missing!")
                return None
            else:
                print("Access Driver found.")
            self.connection, self.cursor = self.connecttodb(path)

    def checkdriver(self):
        for i in pyodbc.drivers():
            if i.startswith('Microsoft Access Driver'):
                return True
            else:
                return False

    def connecttodb(self, path: str):
        connection = pyodbc.connect(path)
        cursor = connection.cursor()
        """
        for i in cursor.tables(tableType='TABLE'):
            print(i.table_name)
        for i in cursor.tables(tableType='VIEW'):
            print(i.table_name)
        """
        print("Connection established.")
        return connection, cursor

    def importdata(self) -> pd.DataFrame:
        data = pd.read_sql('select * from [analysis]', self.connection)
        return data

# pipelines
def createpipeDTR():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=DecisionTreeRegressor(max_depth=10, splitter="random", max_leaf_nodes=None, min_samples_leaf=1)
    #estimator=DecisionTreeRegressor()
    #estimator = KNeighborsRegressor()
    #estimator = MLPRegressor()
    estimator = XGBRegressor(num_parallel_tree=1)
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

# import raw data in csv format
def importdata():
    dbc = db_connection()
    data = dbc.importdata()
    print("Data import successful.")

    X, y = preparedata(data)
    print("Data preparation successful.")

    # split data into training and validation datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def preparedata(data: pd.DataFrame):
    # drop columns so MLA doesnt get biased.
    #data.drop(columns=["ftur"], inplace=True) # 2, 3
    #data.drop(columns=["fpH"], inplace=True)   # 1, 2
    #data.drop(columns=["fEC"], inplace=True)   # 1, 3

    # drop rows with NaN
    data.dropna(axis="index", inplace=True)

    # drop columns to reduce clutter
    data.drop(columns=["swa","fage","Hr","fil","dcp","sssp"], inplace=True)

    #data = data[data["performance"] > 0.5] # 2, 3

    # separate target from features
    #target = ["fpH"]                # 3
    #target = ["fEC"]                # 2
    #target = ["performance", "ftur"] # 1
    target = ["performance", "ftur", "fEC", "fpH"]
    y = data[target]
    data.drop(columns=target, inplace=True)

    return data, y

# assess pipeline
def assess_pipeline(pipe: Pipeline, X_train, X_test, y_train, y_test):
    # actual vs predicted data
    pred_test = pipe.predict(X_test.values)
    df_pred_test = pd.DataFrame.from_dict(pred_test)
    #df_pred_test.rename(columns={0: "ftur", 1: "fpH", 2: "fEC"}, errors= "raise", inplace=True)
    df_pred_test.rename(columns={0: "ftur"}, errors= "raise", inplace=True)
    actualvpredicted = pd.concat([y_test.round(decimals=2).reset_index(), df_pred_test.round(decimals=2)], axis=1)
    actualvpredicted.set_index("index", inplace=True)
    actualvpredicted.to_csv(config.exp_path, sep=";", decimal=",")

    # scores
    rows = len(actualvpredicted.index)
    train_score = pipe.score(X_train.values, y_train)
    test_score = pipe.score(X_test.values, y_test)
    used_features = pipe[2].get_support(indices=True)
    scores = {"rows": rows, "train_score": train_score, "test_score": test_score, "used_features": used_features}
    
    # calculated errors
    rmse = np.sqrt(MSE(y_test, pred_test))
    mae = MAE(y_test,pred_test)
    mape = MAPE(y_test,pred_test)
    evaluation = {"rmse": rmse, "mae": mae, "mape": mape}

    return actualvpredicted, scores, evaluation

X_train, X_test, y_train, y_test = importdata()

pipe = createpipeDTR()
pipe.fit(X_train.values, y_train)
print("new pipe trained.")

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
#print ("MAPE: %.2f" %(evaluation["mape"]))
#print('Accuracy: %.2f'%((100-evaluation["mape"])))