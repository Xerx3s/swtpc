from dataclasses import dataclass
import pandas as pd
from scipy.interpolate import LinearNDInterpolator, RegularGridInterpolator
import matplotlib. pyplot as plt
import numpy as np

from aaa_doser.scripts.modules.connectdb import connectdb

@dataclass
class dc_compC:
    cCl: float = 0
    cSO4: float = 0
    cHCO3: float = 0
    cHPO4: float = 0
    cAs: float = 0

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

        self.compdata = connectdb().compdatatodf()

    def comp_AAA_reduction(self, compC: dc_compC):
        red_Cl = np.interp(compC.cCl,self.compdata.index, self.compdata["Cl"])
        red_SO4 = np.interp(compC.cSO4,self.compdata.index, self.compdata["SO4"])
        red_HCO3 = np.interp(compC.cHCO3,self.compdata.index, self.compdata["HCO3"])
        red_HPO4 = np.interp(compC.cHPO4,self.compdata.index, self.compdata["HPO4"])
        red_As = np.interp(compC.cAs,self.compdata.index, self.compdata["As"])

        return (1+red_Cl) * (1+red_SO4) * (1+red_HCO3) * (1+red_HPO4) * (1+red_As)

    def interpolate(self, time: float, concentration: float,
                    cCl: float = 0, cSO4: float = 0, cHCO3: float = 0,
                    cHPO4: float = 0, cAs: float = 0):
        
        compC = dc_compC(cCl, cSO4, cHCO3, cHPO4, cAs)

        try:
            itp = RegularGridInterpolator(points=[self.C.T[0],self.Time[0]], values=self.Q, method='nearest')
            theo_ad = itp([[concentration,time]])[0]
            comp_red = self.comp_AAA_reduction(compC)
            return theo_ad * comp_red
        except ValueError:
            return "ERROR"