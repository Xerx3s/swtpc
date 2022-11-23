# configuration
from sklearn.pipeline import Pipeline
from . import config
import optunity as op
import pandas as pd
from sklearn.model_selection import cross_validate
def create_objectivefunction(pipe: Pipeline):
    def objectivefunction(swa = None, ipH = None, iEC = None, itur = None, fage = None, Hr = None, salM = None, fil = None, fdose = None, sscp = None, dcp = None, ssfp = None, dfp = None, sssp = None, dsp = None):
        rawinputlist = [swa, ipH, iEC, itur, fage, Hr, salM, fil, fdose, sscp, dcp, ssfp, dfp, sssp, dsp]
        new_input = [[x for x in rawinputlist if x is not None]]
        new_output = pipe.predict(new_input)

        # calculate penalties for performance, fpH and fEC
        total_score = (penalty_ftur(new_output[0][0], itur) * config.pen_ftur
                    + penalty_performance(new_output[0][0]) * config.pen_per
                    + penatly_fpH(new_output[0][1]) * config.pen_fpH
                    + penalty_fEC(new_output[0][2]) * config.pen_fEC)
        
        return new_output[0][0] # maximize only performance
        #return total_score # maximize performance, fpH and fEC
    return objectivefunction

def penalty_performance(performance: float):
    return performance

def penalty_ftur(performance: float, itur: float):
    ftur = (1 - performance) * itur

    if ftur <= 5:
        return 1
    elif ftur > 5 and ftur <= 10:
        return 1
    elif ftur > 10 and ftur <= 20:
        return 0.9
    elif ftur > 20:
        return 0.0
    else:
        return 0

def penatly_fpH(fpH: float):
    if fpH > 7:
        return - fpH / 7 + 2
    elif fpH == 7 :
        return fpH / 7
    elif fpH < 7:
        return fpH / 7
    else:
        return 0

def penalty_fEC(fEC: float):
    if fEC <= 400:
        return 1
    elif fEC > 400 and fEC <= 800:
        return 0.9
    elif fEC > 800 and fEC <= 1400:
        return 0.0
    else:
        return 0

def definelbub(X_train:pd.DataFrame):
    lb = X_train.min()
    ub = X_train.max()
    kwargs_dict = {}

    for index,value in lb.items():
        kwargs_dict[index] = [value, ub[index]+0.1]

    #kwargs_dict["swa"] = config.swa # so kann man einzelne input features auf einen bestimmten Bereich begrenzen

    #print("\nlower and upper borders of used data set:")
    #lbub = pd.DataFrame.from_dict(kwargs_dict, orient="index")
    #print(lbub.round(2))
    return kwargs_dict

def definelbubwithlimits(X_train:pd.DataFrame, limit_lbub: dict):
    lb = X_train.min()
    ub = X_train.max()
    kwargs_dict = {}

    for index,value in lb.items():
        if index in limit_lbub:
            kwargs_dict[index] = [limit_lbub[index], limit_lbub[index]+0.1]
        else:
            kwargs_dict[index] = [value, ub[index]+0.1]

    #kwargs_dict["swa"] = config.swa # so kann man einzelne input features auf einen bestimmten Bereich begrenzen

    #print("\nlower and upper borders of used data set:")
    #lbub = pd.DataFrame.from_dict(kwargs_dict, orient="index")
    #print(lbub.round(2))
    return kwargs_dict

def optimize(pipe: Pipeline, X_train: pd.DataFrame):
    kwargs = definelbub(X_train)
    objectivefunction = create_objectivefunction(pipe)
    optimal_pars, details, _ = op.maximize(objectivefunction, num_evals=config.feature_num, **kwargs)
    return optimal_pars

def optimizewithboders(pipe: Pipeline, X_train: pd.DataFrame, limit_lbub: dict):
    kwargs = definelbubwithlimits(X_train, limit_lbub)
    objectivefunction = create_objectivefunction(pipe)
    optimal_pars, details, _ = op.maximize(objectivefunction, num_evals=config.feature_num, **kwargs)
    return optimal_pars