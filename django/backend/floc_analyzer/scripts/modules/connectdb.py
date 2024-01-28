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

    def flocdatatodf(self):
        df = pds.read_sql("SELECT * FROM db_connection_flocculation_data", self.dbConnection)
        #print(df);
        return(df)

    def flocdataEC(self):
        df = pds.read_sql('SELECT "initial_EC", "floc_concentration", "floc_saline_Molarity", "floc_dose", "floc_vol", "saline_concentration", "final_EC" FROM db_connection_flocculation_data;', self.dbConnection)
        #print(df)
        return(df)

    def flocdatapH(self):
        df = pds.read_sql('SELECT "initial_pH", "floc_concentration", "floc_saline_Molarity", "floc_dose", "final_pH" FROM db_connection_flocculation_data;', self.dbConnection)
        #print(df)
        return(df)

    def flocdataTur(self):
        df = pds.read_sql('SELECT "surface_water", "initial_pH", "initial_EC", "initial_turbidity", "flocculant", "floc_dose", "floc_saline_Molarity", "floc_cactus_share", "stirring_speed_coagulation_phase", "duration_coagulation_phase", "stirring_speed_flocculation_phase", "duration_flocculation_phase", "duration_sedimentation_phase", "final_turbidity" FROM db_connection_flocculation_data;', self.dbConnection)
        #print(df)
        return(df)