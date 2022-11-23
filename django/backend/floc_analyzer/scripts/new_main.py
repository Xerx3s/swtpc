from flocculation_analysis.modules.mlalgorithms import createpipeXGB as createpipeline

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

# import dataset.
dataset = pd.read_excel(r"sustainable-drinking-water-treatment-plant\flocculation_analysis\data\calculations_fEC+fpH.xlsx", sheet_name="ml_fEC")

# prepare dataset. isolate then drop target column.
dataset.drop(columns=["cal_fEC", "d_EC"], inplace=True)
target = ["fEC"]
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