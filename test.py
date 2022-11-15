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

@app.callback(Output(component_id='masterlayout-dynamic-layout', component_property='children'),
              [Input(component_id='masterlayout-selection-tabs-parent', component_property='value'),
              Input(component_id='populationcensus-all_states-dropdown', component_property='value'),
              Input(component_id='populationcensus-state_wise_state-dropdown', component_property='value'),
              Input(component_id='populationcensus-state_wise_metric-dropdown', component_property='value')])

def renderFunction1(value_selected_tab,value_all_metric_states_dropdown,
                   value_populationcensus_state_wise_state_dropdown,
                   value_populationcensus_state_wise_metric_dropdown ):
    
    inputParameter["value_selected_tab"] = value_selected_tab
    inputDict = inputParameter[value_selected_tab]
    inputDict["value_all_states_metric_dropdown"] = value_all_metric_states_dropdown
    inputDict["value_populationcensus_state_wise_state_dropdown"] = value_populationcensus_state_wise_state_dropdown
    inputDict["value_populationcensus_state_wise_metric_dropdown"] = value_populationcensus_state_wise_metric_dropdown
    inputParameter[value_selected_tab] = inputDict
  
    return initialDisplay(DataReader,inputParameter)