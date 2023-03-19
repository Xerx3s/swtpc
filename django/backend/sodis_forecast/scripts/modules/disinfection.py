from math import exp
import pandas as pd

timeExp = 1.3405  # time exponent of Hom's Law
#k1 = 7.709199746 # s^(-timeExp)
k1 = 1800 # new k1 value based on SODIS potential (k_Syn)
k2 = 1.1437e+28
Ea1 = 7417.744722 # both are K-1  (Ea/R)
Ea2 = 22780.93448
alpha = 1.60547561

surface = 0.065 # of bottle (in m²)
surfacetosun = 0.5 # as fraction of surface
heatradiationsun = 0.4 # heat radiation as fraction of the total radiation
mass = 1 # of water (in kg)
c_water = 4181 # thermal capacity of water (in J/(kg*K))
transmittance = 0.9 # of bottle material (dimensionless; value T)
emissivity = 0.91 # of water (as fraction)
boltzmann = 5.67e-8 # constant (in W/(m²*K^4))
lamda = 0.24 # thermal conductivity of PET (in W/(m*K))
materialthickness = 1e-3  # bottle wall thickness (in m)

def SODISkinetics(Tc: float, radiation:float, elapsedTS:float, timestep:float) -> float:
    """
    The central element of the SODIS_Forecaster. This function contains the formula
    used to calculate the logarithmic disinfection.

    References
    ----------
    [1]	Moreno-SanSegundo, José ; Giannakis, Stefanos ; Samoili, Sofia ;
            Farinelli, Giulio ;McGuigan, Kevin G. ; Pulgarín, César ; Marugán, Javier:
        SODIS potential: A novel parameter to assess the suitability of solar water
            disinfection worldwide.
        In: Chemical Engineering Journal 419 (2021), S. 129889.
        URL https://www.sciencedirect.com/science/article/pii/S138589472101473X 
    """
    # Referenz anpassen!

    Tk = 273.0 + Tc
    instantKinetics = k1 * pow((radiation), alpha) * exp(-Ea1 / Tk) + k2 * exp(-Ea2 / Tk)
    addition = instantKinetics * (pow(elapsedTS + timestep, timeExp) - pow(elapsedTS, timeExp))
    return addition

def tempchange(wattemp:float, Tc: float, radiation:float, timestep:float):
    """
    This function calculates the temerature change of the water.
    """
    wattemp = 273.0 + wattemp
    Tk = 273.0 + Tc
    base = (surface * timestep.total_seconds())/(mass * c_water)
    tempchange_sun = base * heatradiationsun * surfacetosun * transmittance * radiation
    tempchange_heatdiss = base * emissivity * boltzmann * (pow(wattemp,4) - pow(Tk,4))
    # Material der Flasche wird bei Dissipation der Wärme nicht beachtet! Einprogrammieren!
    tempchange = tempchange_sun - tempchange_heatdiss
    return tempchange_sun, tempchange_heatdiss, tempchange

def disinfectionuntil(raddata: pd.DataFrame, starttime: pd.Timestamp, wattemp: int = 12, target: int = 4):
    """
    Function to calculate the disinfection and temperaure changes for each given timestep.
    """
    elapsedTS = pd.Timedelta(minutes=0.0) # in min
    timestep = pd.Timedelta(minutes=15.0) # in min
    logdis = 0.0
    nowtime = starttime
    message = ""
    msg_count = 0

    disinfectiondata = pd.DataFrame({"Water Temp": wattemp, "Temp Change": 0, "Temp Change sun": 0, "Temp Change diss": 0, "Log Dis": 0}, index=[starttime])

    while (logdis < target):
        nowdata = raddata.loc[nowtime]
        radiation = nowdata["ghi_cloudy"]
        #radiation = 800
        if radiation == 0:
            message += "Not enough Suntime left. Max log disinfection possible: %.2f.\n" %logdis
            break
        Tc = nowdata["temp_air"]
        #Tc = 30.0
        if Tc < 20 and msg_count == 0:
            #message = "It's too cold (below 20°C) to use SODIS for disinfection."
            message += "Due to the low ambient temperature (below 20 °C), the prediction is not reliable.\n"
            msg_count = 1
            #break
        #print("Radiation: %d" %radiation)
        #print("Air temperature: %.2f" %Tc)
        sun, diss, change = tempchange(wattemp, Tc, radiation, timestep)
        wattemp += change
        #print("Water temperature: %.2f" %wattemp)
        logdis += SODISkinetics(Tc, radiation, elapsedTS.total_seconds()/60, timestep.total_seconds()/60)
        nowtime += timestep
        elapsedTS = nowtime - starttime
        #print("Time (min): ", elapsedTS)
        #print("log disinfection: %.2f\n " %logdis)
        data = pd.DataFrame({"Water Temp": wattemp, "Temp Change": change, "Temp Change sun": sun, "Temp Change diss": -diss, "Log Dis": logdis}, index=[nowtime])
        disinfectiondata = pd.concat([disinfectiondata,data])
    
    duration = (nowtime - starttime).seconds/60/60
    if message == "":
        message = "Requested log disinfection of %d is achieved after %s hours." %(target, duration)
    return disinfectiondata, message, duration
