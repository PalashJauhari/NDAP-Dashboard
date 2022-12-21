import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html

from data import DataReader
from masterlayout import masterLayout
from populationcensus import populationcensusLayout
from callbacks import UIDisplay


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',"/assets/masterlayout.css"]
app = DashProxy(__name__,external_stylesheets=external_stylesheets,transforms=[MultiplexerTransform()],
                prevent_initial_callbacks=False)

# Master Layout
app.layout = masterLayout()

# Import data reader module
DataReader = DataReader()

# This is the input json file used to pass intput to callback functions.
f = open("inputParameters.json")
inputParameter  = json.load(f)



@app.callback(Output(component_id='masterlayout-dynamic-layout', component_property='children'),
              [Input(component_id='masterlayout-selection-tabs-parent', component_property='value')])

def renderFunction(value_selected_tab):
    inputParameter["value_selected_tab"] = value_selected_tab
    return UIDisplay(DataReader,inputParameter)

@app.callback(Output(component_id='masterlayout-dynamic-layout', component_property='children'),
              [Input(component_id='populationcensus-all_states-dropdown', component_property='value'),
               Input(component_id='populationcensus_state_wise_state_dropdown', component_property='value'),
               Input(component_id='populationcensus_state_wise_metric_dropdown', component_property='value')])

def renderFunction1(value_all_metric_states_dropdown,
                   value_populationcensus_state_wise_state_dropdown,
                   value_populationcensus_state_wise_metric_dropdown ):

    inputDict = inputParameter[inputParameter["value_selected_tab"]]
    inputDict["value_all_states_metric_dropdown"] = value_all_metric_states_dropdown
    inputDict["value_populationcensus_state_wise_state_dropdown"] = value_populationcensus_state_wise_state_dropdown
    inputDict["value_populationcensus_state_wise_metric_dropdown"] = value_populationcensus_state_wise_metric_dropdown
    inputParameter[inputParameter["value_selected_tab"]] = inputDict
  
    return UIDisplay(DataReader,inputParameter)

@app.callback(Output(component_id='masterlayout-dynamic-layout', component_property='children'),
              [Input(component_id='socioeconomic-all_states-dropdown', component_property='value'),
               Input(component_id='socioeconomic_state_wise_state_dropdown', component_property='value'),
               Input(component_id='socioeconomic_state_wise_metric_dropdown', component_property='value')])

def renderFunction2(value_all_metric_states_dropdown,
                   value_populationcensus_state_wise_state_dropdown,
                   value_populationcensus_state_wise_metric_dropdown ):

    inputDict = inputParameter[inputParameter["value_selected_tab"]]
    inputDict["value_all_states_metric_dropdown"] = value_all_metric_states_dropdown
    inputDict["value_socioeconomic_state_wise_state_dropdown"] = value_populationcensus_state_wise_state_dropdown
    inputDict["value_socioeconomic_state_wise_metric_dropdown"] = value_populationcensus_state_wise_metric_dropdown
    inputParameter[inputParameter["value_selected_tab"]] = inputDict
  
    return UIDisplay(DataReader,inputParameter)



    
if __name__ == "__main__":
    app.run_server()