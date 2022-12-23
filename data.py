import pandas as pd
import numpy as np

class DataReader():

    def __init__(self):

        self.data_folder_location = "State Data"

    def extractSocioEconomicData(self):

        # Read Raw Data Frames
        df_household = pd.read_csv(self.data_folder_location+"/socioeconomic_household.csv")
        df_electricity_toilets = pd.read_csv(self.data_folder_location+"/socioeconomic_electricity_toilets.csv")
        df_banking = pd.read_csv(self.data_folder_location+"/socioeconomic_banking.csv")
        df_cooking_gas = pd.read_csv(self.data_folder_location+"/socioeconomic_cooking_gas.csv")
        df_ginni = pd.read_csv(self.data_folder_location+"/socioeconomic_ginni.csv")

        # Households
        # combine rural and urban
        df_household_sum = df_household.drop(columns="Residence_Type").groupby("State").sum()
        df_household_sum = df_household_sum.reset_index()
        df_household_sum["Residence_Type"] = "All"
        df_household = pd.concat([df_household,df_household_sum],axis=0)
        df_household = df_household.reset_index().drop(columns="index")
        
        df_household["Normal Households %"] = 100*df_household["Normal Households"]/df_household["Households"] 
        df_household["Institutional Households %"] = 100*df_household["Institutional Households"]/df_household["Households"] 
        df_household["Houseless Households %"] = 100 - df_household["Institutional Households %"] - df_household["Normal Households %"]

        # Electricity and Toilets
        # combine rural and urban
        df_electricity_toilets.rename(columns = {'Households with electricity and latrine facility':"Electricity & Toilets",
                                         'Households without electricity and latrine facility':"None",
                                         'Households with electricity facility':"Only Electricity",
                                         'Households with latrine facility':"Only Toilets"},inplace=True)
        
        df_electricity_toilets_sum = df_electricity_toilets.drop(columns="Residence_Type").groupby("State").sum().reset_index()
        df_electricity_toilets_sum["Residence_Type"] = "All"
        df_electricity_toilets = pd.concat([df_electricity_toilets,df_electricity_toilets_sum ],axis=0)
        
        df_electricity_toilets["Electricity & Toilets %"] = 100*df_electricity_toilets["Electricity & Toilets"]/df_electricity_toilets['Number of households']
        df_electricity_toilets["Only Electricity %"] = 100*df_electricity_toilets["Only Electricity"]/df_electricity_toilets['Number of households']
        df_electricity_toilets["Only Toilets %"] = 100*df_electricity_toilets["Only Toilets"]/df_electricity_toilets['Number of households']
        df_electricity_toilets["None %"] = 100-df_electricity_toilets["Electricity & Toilets %"]-df_electricity_toilets["Only Electricity %"]-df_electricity_toilets["Only Toilets %"]

        # Cooking Gas
        # combine rural and urban
        df_cooking_gas_sum = df_cooking_gas.drop(columns = "Residence_Type").groupby("State").sum().reset_index()
        df_cooking_gas_sum["Residence_Type"] = "All"
        df_cooking_gas = pd.concat([df_cooking_gas,df_cooking_gas_sum],axis=0)
        
        df_cooking_gas['Cowdung/Coal/Wood %'] = 100*df_cooking_gas['Cowdung/Coal/Wood']/df_cooking_gas['Number of households']
        df_cooking_gas['Kerosene %'] = 100*df_cooking_gas['Kerosene']/df_cooking_gas['Number of households']
        df_cooking_gas['Gas Cylinder %'] = 100*df_cooking_gas['Gas Cylinder']/df_cooking_gas['Number of households']
        df_cooking_gas['Others %'] = 100 - df_cooking_gas['Cowdung/Coal/Wood %'] - df_cooking_gas['Kerosene %'] - df_cooking_gas['Gas Cylinder %']

        # Banking
        # combine rural and urban
        df_banking_mean = df_banking.drop(columns="Residence_Type").groupby("State").mean().reset_index()
        df_banking_mean["Residence_Type"]="All"
        df_banking = pd.concat([df_banking,df_banking_mean],axis=0)

        #Ginni
        # combine rural and urban
        df_ginni_mean = df_ginni.drop(columns="Residence_Type").groupby("State").mean().reset_index()
        df_ginni_mean["Residence_Type"]="All"
        df_ginni = pd.concat([df_ginni,df_ginni_mean])
        df_ginni["Gini's coefficient"]=df_ginni["Gini's coefficient"].apply(lambda x : np.round(x,2))


        return df_household,df_electricity_toilets,df_cooking_gas,df_banking,df_ginni 

    
    def extractPopulationCensusData(self):

        df = pd.read_csv(self.data_folder_location+"/State_Population_Census.csv")

        df['Population %'] = 100*df['Population']/(np.sum(df['Population']))
        df['Population %']=df['Population %'].apply(lambda x : str(np.round(x,1))+" %")
        
        # Caste
        
        df['Scheduled caste population %'] = 100*df['Scheduled caste population']/(1+df['Population'])
        df['Male scheduled caste population %'] = 100*df['Male scheduled caste population']/(1+df['Male population'])
        df['Female scheduled caste population %'] = 100*df['Female scheduled caste population ']/(1+df['Female population'])
        
        df['Scheduled tribe population %'] = 100*df['Scheduled tribe population']/(1+df['Population'])
        df['Male scheduled tribe population %'] = 100*df['Male scheduled tribe population']/(1+df['Male population'])
        df['Female scheduled tribe population %'] = 100*df['Female scheduled tribe population ']/(1+df['Female population'])

        df["Gen/OBCs & Others"] = df['Population'] - df['Scheduled caste population'] - df['Scheduled tribe population']
        df["Male Gen/OBCs & Others"] = df['Male population']-df['Male scheduled caste population']-df['Male scheduled tribe population']
        df["Female Gen/OBCs & Others"] = df['Female population']-df['Female scheduled caste population ']-df['Female scheduled tribe population ']
        
        df["Gen/OBCs & Others %"] =  100 - df['Scheduled caste population %'] - df['Scheduled tribe population %'] 
        df["Male Gen/OBCs & Others %"] = 100 - df['Male scheduled caste population %'] - df['Male scheduled tribe population %'] 
        df["Female Gen/OBCs & Others %"] = 100 - df['Female scheduled caste population %'] - df['Female scheduled tribe population %'] 

        #df['Scheduled caste population %'] = df['Scheduled caste population %'].apply(lambda x : np.round(x,1))
        #df['Scheduled tribe population %'] = df['Scheduled tribe population %'].apply(lambda x : np.round(x,1))
        #df["Gen/OBCs & Others %"] = df["Gen/OBCs & Others %"].apply(lambda x : np.round(x,1))
        
        # Literacy

        df['Illiterate population'] = df['Population'] - df['Literate population ']
        df['Illiterate population %'] = 100*df['Illiterate population'] /(1+ df['Population'])
        df['Literate population %'] = 100 - df['Illiterate population %']

        df['Male illiterate population %'] = 100*df['Male illiterate population ']/(1+df['Male population'])
        df['Female illiterate population %'] = 100*df['Female illiterate population ']/(1+df['Female population'])

        df['Male literate population %'] = 100-df['Male illiterate population %']
        df['Female literate population %'] = 100 - df['Female illiterate population %']

        
        # Working
        df['Non Working population'] = df['Population'] - df['Working population']
        df['Working population %'] = 100*df['Working population']/df['Population'] 
        df['Non Working population %'] = 100 - df['Working population %']

        df['Male working population %'] = 100*df['Male working population']/(1+df['Male population'])
        df['Female woking population %'] = 100*df['Female woking population']/(1+df['Female population'])

        df['Male non working population %'] = 100-df['Male working population %']
        df['Female non woking population %'] = 100-df['Female woking population %']


        return df
    
    def extractEducationParticipationData(self):

        # Read Raw Data Frames
        df_attendence_age = pd.read_csv(self.data_folder_location+"/State_Attendance_Age.csv")
        df_attendence_education_level = pd.read_csv(self.data_folder_location+"/State_Attendance_EducationLevel.csv")
        df_courses = pd.read_csv(self.data_folder_location+"/State_Course_Type.csv")
        df_enrollement_education_level = pd.read_csv(self.data_folder_location+"/State_Enrollement_EducationLevel.csv")
        df_institute_course = pd.read_csv(self.data_folder_location+"/State_InstituteType_Course.csv")

        return df_attendence_age,df_attendence_education_level,df_courses,df_enrollement_education_level,df_institute_course
