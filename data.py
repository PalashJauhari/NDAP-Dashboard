import pandas as pd
import numpy as np

class DataReader():

    def __init__(self):
        self.data_folder_location = "State Data"
    
    def extractPopulationCensusData(self):

        df = pd.read_csv(self.data_folder_location+"/State_Population_Census.csv")
        
        # Caste
        df["Gen/OBCs & Others"] = df['Population'] - df['Scheduled caste population'] - df['Scheduled tribe population']
        df["Male Gen/OBCs & Others"] = df['Male population']-df['Male scheduled caste population']-df['Male scheduled tribe population']
        df["Female Gen/OBCs & Others"] = df['Female population']-df['Female scheduled caste population ']-df['Female scheduled tribe population ']

        df['Scheduled caste population %'] = 100*df['Scheduled caste population']/(1+df['Population'])
        df['Scheduled tribe population %'] = 100*df['Scheduled tribe population']/(1+df['Population'])
        df["Gen/OBCs & Others %"] =  100 - df['Scheduled caste population %'] - df['Scheduled tribe population %'] 
        
        # Literacy

        df['Illiterate population'] = df['Population'] - df['Literate population ']
        df['Illiterate population %'] = 100*df['Illiterate population'] /(1+ df['Population'])
        df['Literate population %'] = 100-df['Illiterate population %']

        # Working
        df['Non Working population'] = df['Population'] - df['Working population']
        df['Working population %'] = 100*df['Working population']/df['Population'] 
        df['Non Working population %'] = 100 - df['Working population %']
    

    
        return df
