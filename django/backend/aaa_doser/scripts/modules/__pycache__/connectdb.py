import psycopg2
import pandas as pds
from sqlalchemy import create_engine
import environ

env = environ.Env()
environ.Env.read_env()

class connectdb:
    def __init__(self):
        self.alchemyEngine = create_engine(env('alchemy_create_engine_path'))
        self.dbConnection = self.alchemyEngine.connect()
        #print("connected")

    def __del__(self):
        #print("garbage collected")
        self.dbConnection.close()

    def aaadatatostackeddf(self):
        df = pds.read_sql("SELECT * FROM db_connection_aaa_data", self.dbConnection)
        return(df)
    
    def compdatatodf(self):
        df = pds.read_sql("SELECT * FROM db_connection_aaa_comp_data", self.dbConnection)
        return(df)