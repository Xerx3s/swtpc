import pyodbc
import pandas as pd
import flocculation_analysis.modules.config as config

class db_connection:

    def __init__(self, path: str = config.db_path):
            if self.checkdriver():
                print("Access Driver missing!")
                return None
            else:
                print("Access Driver found.")
            self.connection, self.cursor = self.connecttodb(path)

    def checkdriver(self):
        for i in pyodbc.drivers():
            if i.startswith('Microsoft Access Driver'):
                return True
            else:
                return False

    def connecttodb(self, path: str):
        connection = pyodbc.connect(path)
        cursor = connection.cursor()
        """
        for i in cursor.tables(tableType='TABLE'):
            print(i.table_name)
        for i in cursor.tables(tableType='VIEW'):
            print(i.table_name)
        """
        print("Connection established.")
        return connection, cursor

    def importdata(self) -> pd.DataFrame:
        data = pd.read_sql('select * from [analysis]', self.connection)
        return data

    """ add correct parameter names!
    def insertnewdata(self, params: tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]):
        self.cursor.execute("insert into [analysis] (d, s1, s1h, s1minK, s1maxK, s1meanK, minQ, maxQ, meanQ, minP, maxP, meanP, tbio, iecoli, fecoli, itur, ftur) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        self.cursor.commit()
        print("new Data added successfully")
    """

"""
dbc = db_connection()
print(dbc.importdata())
"""

"""
params = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
dbc.insertnewdata(params)
"""