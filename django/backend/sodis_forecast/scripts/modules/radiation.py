import pandas as pd
import numpy as np
from timezonefinder import TimezoneFinder
from pvlib.location import Location
from pvlib.irradiance import disc
import datetime
from pyowm import OWM
import pytz
import requests
import json

class SunRadiationCalculator:
    """
    initializing this class gives the option to use its contained functions.
    """
    def __init__(self, latitude: float, longitude: float, altitude: float = 0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.timezonename = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
        self.tz = pytz.timezone(self.timezonename)

    def settime(self, hour: int = None):
        """
        Uses the given hour to return a starting time. \n
        if the given hour is past the current one, it is assumend,
        that the user wants so see the results for the next day.
        """
        nowhour = datetime.datetime.now(tz=self.tz).hour

        if hour != None:
            if hour > nowhour:
                # specify starting hour on same day
                starttime = datetime.datetime.now(tz=self.tz).replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                # specify starting hour on next day
                starttime = datetime.datetime.now(tz=self.tz).replace(hour=hour, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        else:
            # use current hour
            starttime = datetime.datetime.now(tz=self.tz).replace(minute=0, second=0, microsecond=0)
        return starttime

#    def owm_sunriseset(self):
#        owm = OWM("a9c05d43e3817e2b68f4f0f305504cf7")
#        mgr = owm.weather_manager()
#        one_call = mgr.one_call(lat=self.latitude, lon=self.longitude)
#
#        return one_call.current.sunrise_time(), one_call.current.sunset_time()
#
#
#    def owm_onecall(self):
#        """
#        Uses the openweathermap one call api to receive the weather
#        information for the next 48 hours. \n
#        The returned DataFrame is in the format "time": ["temp_air", "total_clouds"].
#        """
#        owm = OWM("a9c05d43e3817e2b68f4f0f305504cf7")
#        mgr = owm.weather_manager()
#        one_call = mgr.one_call(lat=self.latitude, lon=self.longitude)
#
#        df = pd.DataFrame()
#        for entry in one_call.forecast_hourly:
#            time = entry.reference_time("date")
#            local_time = time.astimezone(self.tz)
#            data = {"time": local_time, "temp_air": entry.temperature("celsius").get("temp"), "total_clouds": entry.clouds}
#            df_data = pd.DataFrame.from_dict([data])
#            df = pd.concat([df, df_data])
#        df.set_index("time", inplace=True)
#        return df

    def owm_onecall(self):
        """
        Uses the openweathermap one call api to receive the weather
        information for the next 48 hours. \n
        The returned DataFrame is in the format "time": ["temp_air", "total_clouds"].
        """

        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={self.latitude}&lon={self.longitude}&appid=39fd1dbcf403fd3168825b4ee1a2ffde&units=metric'
        r = requests.get(url)
        one_call = r.json()

        df = pd.DataFrame()
        for entry in one_call["hourly"]:
            time = datetime.datetime.fromtimestamp(entry["dt"], pytz.timezone(one_call["timezone"]))
            data = {"time": time, "temp_air": entry["temp"], "total_clouds": entry["clouds"]}
            df_data = pd.DataFrame.from_dict([data])
            df = pd.concat([df, df_data])
        df.set_index("time", inplace=True)
        return df

    def cloud_cover_to_ghi_linear(self, cloud_cover, ghi_clear, offset=35,
                                  **kwargs):
        """
        Convert cloud cover to GHI using a linear relationship.
        0% cloud cover returns ghi_clear.
        100% cloud cover returns offset*ghi_clear.

        Parameters
        ----------
        cloud_cover: numeric
            Cloud cover in %.
        ghi_clear: numeric
            GHI under clear sky conditions.
        offset: numeric, default 35
            Determines the minimum GHI.
        kwargs
            Not used.

        Returns
        -------
        ghi: numeric
            Estimated GHI.

        References
        ----------
        Larson et. al. "Day-ahead forecasting of solar power output from
        photovoltaic plants in the American Southwest" Renewable Energy
        91, 11-20 (2016).
        """

        offset = offset / 100.
        cloud_cover = cloud_cover / 100.
        ghi = (offset + (1 - offset) * (1 - cloud_cover)) * ghi_clear
        return ghi

    def get_radiationdata(self, starttime: datetime.datetime) -> pd.DataFrame:
        """
        This function is the core of the class. It uses given parameters to calculate the
        radiation data at a specific location.
        """
        loc = Location(latitude=self.latitude, longitude=self.longitude, tz=self.timezonename, altitude=self.altitude)
        endtime = starttime + datetime.timedelta(days=2)
        #starttime = starttime - datetime.timedelta(hours=5)
        times = pd.date_range(start=starttime, end=endtime, freq='1h', tz=self.timezonename)
        cs = loc.get_clearsky(times)  # ineichen with climatology table by default
        solpos = loc.get_solarposition(times)
        cs.index.name = "time"
        solpos.index.name = "time"
        
        weather_data = self.owm_onecall()
        
        # Hier wird die Zeitzone auf UTC geändert!
        data = cs.join(weather_data, lsuffix='_cs', rsuffix='_wd')
        data["ghi_cloudy"] = data.apply(lambda row : self.cloud_cover_to_ghi_linear(cloud_cover= row["total_clouds"], ghi_clear= row["ghi"]), axis=1)

        dni_cloudy = disc(ghi=data["ghi_cloudy"], solar_zenith=solpos["zenith"], datetime_or_doy=data.index)
        data = data.join(dni_cloudy["dni"], lsuffix='', rsuffix='_cloudy')

        dhi_cloudy = data["ghi_cloudy"] - data["dni_cloudy"] * np.cos(np.radians(solpos['zenith']))
        dhi_cloudy.rename("dhi_cloudy", inplace=True)
        data = data.join(dhi_cloudy, lsuffix='', rsuffix='_cloudy')

        #data.drop(["ghi", "dni", "dhi"], axis=1, inplace=True)
        #data.rename(columns={"ghi_cloudy": "ghi", "dni_cloudy": "dni", "dhi_cloudy": "dhi"}, inplace=True)

        data.dropna(inplace=True)
        data = data.resample("15min").interpolate()

        #return data[["ghi", "temp_air", "total_clouds"]]
        return data