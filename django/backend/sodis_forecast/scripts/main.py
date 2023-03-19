from sodis_forecast.scripts.modules.radiation import getlocation
from sodis_forecast.scripts.modules.radiation import SunRadiationCalculator as SRC
from sodis_forecast.scripts.modules.disinfection import disinfectionuntil

def sodis_forecast(
    location: dict = {"city": "Darmstadt", "country": "Deutschland"},
    hour: int = 8.0,
    wattemp: int = 18,
    tarlogdis: int = 4):
    """
    This Function uses given input parameters to predict the
    possible irradiance and temperature of a specific location. \n
    As a result a DataFrame of the format 'time': ['total Radiation', 'Air Temp', 'total Clouds', 'actual Radiation',
    'Water Temp', 'Temp Change', 'Temp Change sun', 'Temp Change diss',
    'Log Dis'] is returned. \n
    Additionally a message is returned containing if and why the target disinfection could not be reached.
    """

    print("Forecast in %s at %.2f" %(location["city"], hour))
    loc = getlocation(location["country"], location["city"])
    radcal = SRC(loc[0], loc[1], loc[2])
    starttime = radcal.settime(hour)
    raddata = radcal.get_radiationdata(starttime)
    disdata, message, duration = disinfectionuntil(raddata, starttime, wattemp, tarlogdis)
    result = raddata.join(disdata)
    result.drop(["dni", "dhi", "dni_cloudy", "dhi_cloudy"], axis=1, inplace=True)
    result.rename({"ghi": "total Radiation", "ghi_cloudy": "actual Radiation", "temp_air": "Air Temp", "total_clouds": "total Clouds"}, axis=1, inplace=True)
    result.dropna(inplace=True)

    output = result[["actual Radiation", "total Clouds", "Air Temp", "Water Temp", "Log Dis"]]
    return output, message, duration