import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from joblib import dump, load
import floc_analyzer.scripts.modules.config as config

# pipelines
def createpipeDTR():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=DecisionTreeRegressor(max_depth=10, splitter="random", max_leaf_nodes=None, min_samples_leaf=1)
    estimator=DecisionTreeRegressor()
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def createpipeRFR():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=RandomForestRegressor(max_depth=None, bootstrap=False, n_estimators=800, min_samples_split=2, min_samples_leaf=1)
    estimator=RandomForestRegressor()
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def createpipeXGB():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=xgb.XGBRegressor(n_estimators=100, max_depth=5, eta=0.9, subsample=0.7, colsample_bytree=0.5, scale_pos_weight=5)
    estimator=xgb.XGBRegressor()
    #estimator=xgb.XGBRegressor(eta=0.1, gamma=0, max_depth=10, min_child_weight=1, subsample=0.6,
    #                            colsample_bytree=0.7, tree_method="exact", num_parallel_tree=1)
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def createpipeLASSO():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=DecisionTreeRegressor(max_depth=10, splitter="random", max_leaf_nodes=None, min_samples_leaf=1)
    estimator=Lasso()
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def createpipeMLP():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=DecisionTreeRegressor(max_depth=10, splitter="random", max_leaf_nodes=None, min_samples_leaf=1)
    estimator=MLPRegressor()
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def createpipeKN():
    imputer=SimpleImputer(missing_values=np.nan, strategy="mean")
    scaler=StandardScaler()
    selector=VarianceThreshold(threshold=(0.8*(1-0.8)))
    #estimator=DecisionTreeRegressor(max_depth=10, splitter="random", max_leaf_nodes=None, min_samples_leaf=1)
    estimator=KNeighborsRegressor()
    pipe = make_pipeline(imputer, scaler, selector, estimator)
    return pipe

def assess_pipeline(pred_type, pipe: Pipeline, X_train, X_test, y_train, y_test):
    # actual vs predicted data
    pred_test = pipe.predict(X_test.values)
    df_pred_test = pd.DataFrame.from_dict(pred_test)
    df_pred_test.rename(columns={0: "prediction"}, errors= "raise", inplace=True)
    actualvpredicted = pd.concat([y_test.round(decimals=2).reset_index(), df_pred_test.round(decimals=2)], axis=1)
    actualvpredicted.set_index("index", inplace=True)
    save_path = "floc_analyzer/data/actualvpredicted/actualvpredicted_" + pred_type + ".txt"
    actualvpredicted.to_csv(save_path, sep=";", decimal=",")

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

# save and load pipeline
def save_pipeline(pipeline, savepath: str):
    dump(pipeline, savepath)

def load_pipeline(loadpath: str):
    pipeline = load(loadpath)
    return pipeline