import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc

def populationcensusLayout():

    """
    This function return UI for population census tab.
    """

    # All States (Left Side Box)

    all_states_metric_dropdown = dcc.Dropdown(options=[{'label': 'Population', 'value': 'population'},
                                                       {'label': 'Caste Distribution', 'value': 'caste_distribution'},
                                                       {'label': 'Literacy', 'value': 'literacy'},
                                                       {'label': 'Employment', 'value': 'employment'}],
                                                       value='population',
                                                       id="populationcensus-all_states-dropdown",
                                                       maxHeight=125)
    all_states = html.Div([all_states_metric_dropdown],id="populationcensus-all_states")
    
    # State Wise (Right Side Box)
    
    state_wise_state_dropdown = dcc.Dropdown(options=[{'label': 'Madhya Pradesh', 'value': 'Madhya Pradesh'},
                                                      {'label': 'Maharashtra', 'value': 'Maharashtra'}],
                                                      value='Maharashtra',
                                            id="populationcensus-state_wise_state-dropdown",
                                            maxHeight=125)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Population', 'value': 'population'},
                                                       {'label': 'Caste Distribution', 'value': 'caste_distribution'},
                                                       {'label': 'Literacy', 'value': 'literacy'},
                                                       {'label': 'Employment', 'value': 'employment'}],
                                                      value='population',
                                            id="populationcensus-state_wise_metric-dropdown",
                                            maxHeight=125)
    
    
    aggregated_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown ],
                                   id="populationcensus-aggregated_metrics")
    #genderwise_metrics = html.Div([],id="populationcensus-genderwise_metrics")

    return html.Div([all_states,aggregated_metrics])