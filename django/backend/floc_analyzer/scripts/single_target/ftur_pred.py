import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_absolute_percentage_error as MAPE

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

def assess_pipeline(pipe: Pipeline, X_train, X_test, y_train, y_test):
    # actual vs predicted data
    pred_test = pipe.predict(X_test.values)
    df_pred_test = pd.DataFrame.from_dict(pred_test)
    df_pred_test.rename(columns={0: "ftur"}, errors= "raise", inplace=True)
    actualvpredicted = pd.concat([y_test.round(decimals=2).reset_index(), df_pred_test.round(decimals=2)], axis=1)
    actualvpredicted.set_index("index", inplace=True)
    actualvpredicted.to_csv(r"parts-testing\flocculation prediction\data\actualvpredicted_ftur.txt", sep=";", decimal=",")

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

# import dataset.
rawdata = pd.read_excel(r"sustainable-drinking-water-treatment-plant\flocculation_analysis\data\calculations_fEC+fpH.xlsx", sheet_name="ml_ftur")

# prepare dataset. isolate then drop target column.
dataset = rawdata.loc[rawdata["sw"].isin(["model suspension",])] # oder .isin(["Mühlbach",])
dataset.drop(columns=["sw", "f"], inplace=True)

target = ["ftur"]
y = dataset[target]
dataset.drop(columns=target, inplace=True)

# split dataset into training and validation datasets
X_train, X_test, y_train, y_test = train_test_split(dataset, y,
                                                    test_size=0.2,
                                                    random_state=42)

pipe = createpipeXGB()

pipe.fit(X_train, y_train)

actualvpredicted, scores, evaluation = assess_pipeline(pipe, X_train, X_test, y_train, y_test)

print(actualvpredicted)

print(scores)

print(evaluation)