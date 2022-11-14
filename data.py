import pandas as pd
import numpy as np

class DataReader():

    def __init__(self):
        self.data_folder_location = "State Data"
    
    def extractPopulationCensusData(self):
        df = pd.read_csv(self.data_folder_location+"/State_Population_Census.csv")

        return df
