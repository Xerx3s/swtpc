import pandas as pd
from scipy.interpolate import LinearNDInterpolator, RegularGridInterpolator
import matplotlib. pyplot as plt
import numpy as np

from aaa_doser.scripts.modules.connectdb import connectdb

class aaa_doser():
    def __init__(self):
        stacked = connectdb().aaadatatostackeddf()
        t = stacked["time"]
        c = stacked["concentration"]
        q = stacked["coverage"]

        Time = np.linspace(min(t), max(t)) # Intervall gleichmäßig unterteilen
        C = np.linspace(min(c), max(c)) #
        self.Time, self.C = np.meshgrid(Time, C)  # 2D-Grid für die Interpolation
        interp = LinearNDInterpolator(list(zip(t, c)), q)
        self.Q = interp(self.Time, self.C)
    def interpolate(self, time: float, concentration: float):
        itp = RegularGridInterpolator(points=[self.C.T[0],self.Time[0]], values=self.Q, method='nearest') 
        return itp([[time,concentration]])[0]