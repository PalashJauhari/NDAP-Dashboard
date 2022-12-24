import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go

def healthLayout(DataReader,inputDict):

    """
    This function return UI for health tab.

    """

    all_states_metric_dropdown = dcc.Dropdown(options=[{'label': 'Women Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Women with High B.P', 'value': 'women_high_bp'},
                                                       {'label': 'Women with High Sugar', 'value': 'women_high_sugar'},
                                                       {'label': 'Men Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Men with High B.P', 'value': 'men_high_bp'},
                                                       {'label': 'Men with High Sugar', 'value': 'men_high_sugar'},
                                                       {'label': 'Infant mortality rate', 'value': 'imr'},
                                                       {'label': 'Fertility Rate', 'value': 'fertility_rate'},
                                                       {'label': 'Sex Ratio', 'value': 'sex_ratio'},
                                                       {"label":'Fully immunised children',"value":"fully_immunised"},
                                                       {"label":'Health Facilities Per unit Population',"value":"health_facility"}],                                                      
                                                       value=inputDict["value_all_states_metric_dropdown"],
                                                       id="health-all_states-dropdown",
                                                       maxHeight=175)
    
    
    all_states = html.Div([all_states_metric_dropdown],id="health-all_states")

    # State Wise (Right Side Box)
    #state_list = [{'label': i, 'value': i} for i in np.unique(df_household["State"].values)]
    state_list = [{'label': "India", 'value': "India"}]
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_health_state_wise_state_dropdown"],
                                            id="health_state_wise_state_dropdown",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Women Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Women with High B.P', 'value': 'women_high_bp'},
                                                       {'label': 'Women with High Sugar', 'value': 'women_high_sugar'},
                                                       {'label': 'Men Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Men with High B.P', 'value': 'men_high_bp'},
                                                       {'label': 'Men with High Sugar', 'value': 'men_high_sugar'},
                                                       {'label': 'Infant mortality rate', 'value': 'imr'},
                                                       {'label': 'Fertility Rate', 'value': 'fertility_rate'},
                                                       {'label': 'Sex Ratio', 'value': 'sex_ratio'},
                                                       {"label":'Fully immunised children',"value":"fully_immunised"}],
                                                      value=inputDict["value_health_state_wise_metric_dropdown"],
                                            id="health_state_wise_metric_dropdown",
                                            maxHeight=175)
    


    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown],
                                   id="health_state_wise_metrics")
    return html.Div([all_states, state_wise_metrics])