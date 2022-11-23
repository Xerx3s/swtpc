import flocculation_analysis.modules.config as config
import pandas as pd
from sklearn.model_selection import train_test_split
from flocculation_analysis.modules.connectdb import db_connection

# import raw data in csv format
def importdata(filepath: str):
    #data = pd.read_csv(filepath, sep=";")
    dbc = db_connection()
    data = dbc.importdata()
    print("Data import successful.")

    X, y = preparedata(data)
    print("Data preparation successful.")

    # split data into training and validation datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.test_dataset_size, random_state=config.rand_state)

    return X_train, X_test, y_train, y_test

def preparedata(data: pd.DataFrame):
    # drop ftur so MLA doesnt get biased.
    data.drop(columns="ftur", inplace=True)

    # drop rows with NaN
    data.dropna(axis="index", inplace=True)

    # drop columns to reduce clutter
    data.drop(columns=["swa","fage","Hr","fil","dcp","sssp"], inplace=True)

    # separate target from features
    target = ["performance", "fpH", "fEC"]
    y = data[target]
    data.drop(columns=target, inplace=True)

    return data, y

def finalizedata(data: pd.DataFrame):
    if "swa" in data[0]:
        data[0]["swa"] = data[0]["swa"].round(0)
    if "ipH" in data[0]:
        data[0]["ipH"] = data[0]["ipH"].round(1)
    if "iEC" in data[0]:
        data[0]["iEC"] = data[0]["iEC"].round(0)
    if "itur" in data[0]:
        data[0]["itur"] = data[0]["itur"].round(0)
    if "fage" in data[0]:
        data[0]["fage"] = data[0]["fage"].round(0)
    if "Hr" in data[0]:
        data[0]["Hr"] = data[0]["Hr"].round(0)
    if "salM" in data[0]:
        data[0]["salM"] = data[0]["salM"].round(2)
    if "fil" in data[0]:
        data[0]["fil"] = data[0]["fil"].round(0)
    if "fdose" in data[0]:
        data[0]["fdose"] = data[0]["fdose"].round(0)
    if "sscp" in data[0]:
        data[0]["sscp"] = data[0]["sscp"].round(0)
    if "dcp" in data[0]:
        data[0]["dcp"] = data[0]["dcp"].round(0)
    if "ssfp" in data[0]:
        data[0]["ssfp"] = data[0]["ssfp"].round(0)
    if "dfp" in data[0]:
        data[0]["dfp"] = data[0]["dfp"].round(0)
    if "sssp" in data[0]:
        data[0]["sssp"] = data[0]["sssp"].round(0)
    if "dsp" in data[0]:
        data[0]["dsp"] = data[0]["dsp"].round(0)

    indexnames={"swa": "surface water age (days)",
                "ipH": "initial pH (-)",
                "iEC": "initial EC (microS/cm)",
                "itur": "initial turbidity (NTU)",
                "fage": "flocculant age (days)",
                "Hr": "Husk removed?",
                "salM": "saline Molarity (mol/l)",
                "fil": "filtered?",
                "fdose": "floc dose (mg/l)",
                "sscp": "stirring speed coagulation phase (rpm)",
                "dcp": "duration coagulation phase (min)",
                "ssfp": "stirring speed flocculation phase (rpm)",
                "dfp": "duration flocculation phase (min)",
                "sssp": "stirring speed sedimentation phase (rpm)",
                "dsp": "duration sedimentation phase (min)"}

    data.rename(index={k: v for k, v in indexnames.items() if v not in data}, inplace=True)

    return data