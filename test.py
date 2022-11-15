import pandas as pd
import numpy as np

df = pd.read_csv("State Data/State_Population_Census.csv")
print(df.columns)

['Population', 'Male population', 'Female population',
       'Scheduled caste population', 'Male scheduled caste population',
       'Female scheduled caste population ', 'Scheduled tribe population',
       'Male scheduled tribe population', 'Female scheduled tribe population ',
       'Literate population ', 'Male literate population',
       'Female literate population ', 'Illiterate population',
       'Male illiterate population ', 'Female illiterate population ',
       'Working population', 'Male working population',
       'Female woking population', 'State']